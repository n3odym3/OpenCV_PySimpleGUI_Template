#!/usr/bin/env python

import cv2
import time 
import math 

class Video:
	def __init__(self,port, api, calibration, unit, distance):
		#Video init
		self.video = cv2.VideoCapture(port,api)
		self.port = port
		self.defined = False

		#Get and save the video informations
		self.theo_fps = self.video.get(cv2.CAP_PROP_FPS)
		self.resolution = self.video.get(cv2.CAP_PROP_FRAME_WIDTH)
		self.totframe = self.video.get(cv2.CAP_PROP_FRAME_COUNT)
		self.framenum = 0
		self.pause = False

		#FPS counter
		self.now = 0
		self.last = 0
		self.fps = 0
		self.fps_mean = 0
		self.fps_sum = 0
		self.fps_mean_imgcounter = 0
		self.fps_txtpos = (5,80)
		self.fps_txtcolor = (0,0,0)
		self.fps_txtsize = 0.75
		self.fps_txtthick = 2

		#Size ref
		self.sizeref_calibration = calibration
		self.sizeref_unit = unit
		self.sizeref_distance = distance
		self.sizeref_txtpos = (5,30)
		self.sizeref_txtcolor = (0,0,255)
		self.sizeref_txtsize = 0.75
		self.sizeref_txtthick = 2
		self.sizeref_linepos = (10,50)
		self.sizeref_linecolor = (0,0,255)

	#Read the next frame
	def read(self):
		ret, frame = self.video.read()
		self.framenum += 1
		self.calc_fps()

		self.fps_mean_imgcounter += 1
		if(self.fps_mean_imgcounter >= self.theo_fps):
			self.fps_mean = self.fps_sum / self.theo_fps
			self.fps_mean_imgcounter, self.fps_sum = 0,0
		else :
			self.fps_sum += self.fps
		return ret, frame

	#Set the reading at a specific frame
	def set_frame(self, frame):
		self.video.set(cv2.CAP_PROP_POS_FRAMES, frame)

	#Stop the video and release the camera
	def stop(self):
		self.defined = False
		self.video.release()

	#Set video resolution (for webcam)
	def set_resolution(self, resolution):
		self.video.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
		self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])

	#Calc the current framerate
	def calc_fps(self):
		self.now = time.time()
		delta = self.now - self.last
		if delta > 0 :
			self.fps = 1/delta
			self.last = self.now
		return self.fps

	#Draw the current framerate on the frame
	def draw_fps(self,frame):
		cv2.putText(frame, "{:.1f} FPS".format(self.fps), self.fps_txtpos, cv2.FONT_HERSHEY_DUPLEX, self.fps_txtsize, self.fps_txtcolor , self.fps_txtthick, cv2.LINE_AA)
		return frame

	#Draw the size reference on the frame
	def draw_sizeref(self,frame):
		cv2.putText(frame, str(self.sizeref_distance) + self.sizeref_unit ,self.sizeref_txtpos, cv2.FONT_HERSHEY_DUPLEX , self.sizeref_txtsize, self.sizeref_txtcolor, self.sizeref_txtthick, cv2.LINE_AA)
		cv2.line(frame, self.sizeref_linepos,(int(self.sizeref_distance / self.sizeref_calibration),self.sizeref_linepos[1] ), self.sizeref_linecolor, 5,cv2.LINE_AA)
		return frame

class Measurement:
	def __init__(self,calibration, unit):
		#Clic 1 and clic 2
		self.p1 = (0,0)
		self.p2 = (0,0)
		self.clicnr = 0

		#Distance
		self.distance = 0
		self.sizeref_calibration = calibration
		self.sizeref_unit = unit
		self.txtcolor = (255,0,0)
		self.txtsize = 0.65
		self.txtthick = 1

	#Measurement with left clic
	def clic(self,frame,point):
		#Cycle trough clic 1 and clic 2
		if self.clicnr < 1 :
			self.clicnr +=1
			self.p1 = point
			return frame
		else :
			self.clicnr = 0
			self.p2 = point
			self.distance = math.dist(self.p1, self.p2)
			cv2.line(frame, self.p1,self.p2, (0,0,255), 3,cv2.LINE_AA)
			cv2.putText(frame, "{:.1f}".format(self.distance * self.sizeref_calibration) + self.sizeref_unit ,(self.p1[0], self.p1[1] +20), cv2.FONT_HERSHEY_DUPLEX , self.txtsize, self.txtcolor, self.txtthick,cv2.LINE_AA)
			return frame
		
class Demo :
	def __init__(self,blur,thresh1, thresh2):
		self.blur = blur
		self.thresh1 = thresh1
		self.thresh2 = thresh2

	def edge_detection(self, frame):
		frame = cv2.GaussianBlur(frame, (self.blur, self.blur), 0)
		frame = cv2.Canny(frame, self.thresh1, self.thresh2)
		return frame