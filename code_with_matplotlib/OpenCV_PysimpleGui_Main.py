#!/usr/bin/env python

import multiprocessing
import cv2
from gui import *
from functions import *
from plot import *

#Multiprocessing Queues==============
#By running the GUI in a different process, the window will stay responsive even if the OpenCV processing slow down the code
from_gui = multiprocessing.Queue(1)
to_gui = multiprocessing.Queue(1)
to_gui_list = []
to_plot = multiprocessing.Queue(1)
#Multiprocessing Queues==============

#Default calibration=================
calibration_distance = 100
calibration_unit = 'px'
calibration_value = 1 #In unit/pixel
#Default calibration=================

#Object construction=======================================================================
video = Video(0, None, calibration_value, calibration_unit, calibration_distance)
measurement = Measurement(calibration_value, calibration_unit)
demo = Demo(3,50,150)
plotgui = PlotGUI()
#Object construction=======================================================================

#OpenCV mouse callback=====================================================================
#This function is triggered when you interact with the frame using your mouse
def mouse_callback(event, x, y, flags, params):
    global frame, tracker, measurement
    match event :
        case cv2.EVENT_LBUTTONDOWN :
            #Measure the distance between two points (using the defined unit/calibration)
            measurement.clic(frame,(x,y))
            cv2.imshow('Frame', frame)
        case cv2.EVENT_RBUTTONDOWN :
            pass
        case cv2.EVENT_MBUTTONDOWN :
            pass
        case  cv2.EVENT_MOUSEMOVE :
            pass  
#OpenCV mouse callback=====================================================================

#MAIN =====================================================================================
if __name__ == '__main__' : 
    multiprocessing.Process(target=gui, args=((window1,window2),from_gui,to_gui,to_plot,), name='gui').start()
    gui_window, gui_event, gui_values = from_gui.get()

    while True:
        #Get events from GUI queue-----------------
        gui_event = 'none'
        if not from_gui.empty() :
            gui_window, gui_event, temp_gui_values = from_gui.get()
            update_values = gui_values
        
            if gui_window == 'W1' and gui_event in (None, 'Exit'):
                    break
            
            if gui_window == 'W1' :
                gui_values = temp_gui_values
            elif gui_window == 'W2' :
                gui_plot_values = temp_gui_values
            elif gui_window == "CANVAS" :
                print(temp_gui_values)
        #Get events from GUI queue-----------------

        #Video-------------------------------------------------------------------------------------
        if video.defined :
            if video.pause is False :
                ret, frame = video.read()

                if ret :
                    #Display the size reference on the frame
                    if gui_values['video-sizeref'] and gui_values['video-show']:
                        video.draw_sizeref(frame)

                    #Display the framerate on the frame
                    if gui_values['video-fps'] and gui_values['video-show'] :
                        video.draw_fps(frame)

                    #Image processing demo....................................
                    if gui_values['demo-edge'] and gui_values['video-show'] :
                        frame = demo.edge_detection(frame)
                    #Image processing demo....................................

                    #Create/display and resize the image window
                    if gui_values['video-show'] :
                        cv2.namedWindow('Frame', cv2.WINDOW_NORMAL)
                        cv2.resizeWindow('Frame', 1280, 720)
                        cv2.imshow('Frame', frame)
                    
                    #Send the current framerate to the GUI
                    current_fps = "FPS : {0:.1f} | {1:.1f}".format(video.fps,video.fps_mean)
                    to_gui_list.append(('W1', 'video-curfps', current_fps))

                #Close the window when the video end
                else :
                    video.stop()
                    cv2.destroyAllWindows()

            #Handle the window and keyboard inputs
            if gui_values['video-show'] :
                key = cv2.waitKey(int(gui_values['video-speed']))
                if key != -1 :
                    print("Key pressed : {}".format(key))

            #Update the GUI progress bar
            if video.totframe > 0 :
                to_gui_list.append(['W1','video-progress',int((100/video.totframe)*video.framenum)])
        #Video-------------------------------------------------------------------------------------
        
        #Handle GUI events-------------------------------------------------------------------------
        #evensplit contain the "group"[0] and "topic"[1] of the event
        if gui_event and gui_event not in ('none', '__TIMEOUT__') :
            eventsplit = gui_event.split('-')
            match eventsplit[0] :
                #Match the groups
                case 'video':
                    #Match the topics of the video group
                    match eventsplit[1] :
                        #Play/pause the video
                        case 'pause' :
                            video.pause = not video.pause 

                        #Update the size calibration
                        case 'updatecal' :
                            #Get the new values from the GUI
                            calibration_unit = gui_values['calibration-unit']
                            calibration_value = float(gui_values['calibration-value'])
                            calibration_distance = float(gui_values['calibration-distance'])

                            #Update the image scale
                            video.sizeref_unit = calibration_unit
                            video.sizeref_calibration = calibration_value
                            video.sizeref_distance = calibration_distance

                            #Update the calibration for the measurement with the mouse
                            measurement.sizeref_unit = calibration_unit
                            measurement.sizeref_calibration = calibration_value
                        
                        #Start the reading of a prerecorded video file
                        case 'startfile' : 
                            file = gui_values['video-folder']
                            print("Reading : {}".format(file))
                            video = Video(file, cv2.CAP_FFMPEG, calibration_value, calibration_unit, calibration_distance)

                            #Display the video resolution and framerate on the GUI
                            video_info = "Res : {0} FPS : {1}".format(video.resolution, video.theo_fps)
                            to_gui_list.append(['W1','video-info',video_info])
                            
                            #Read the first frame
                            ret, frame = video.read()
                            
                            #Create and resize a window and add the mouse callback (only if Show video is ticked) 
                            if gui_values['video-show']:
                                cv2.namedWindow('Frame', cv2.WINDOW_NORMAL)
                                cv2.resizeWindow('Frame', 1280, 720)
                                cv2.setMouseCallback('Frame', mouse_callback)

                            video.defined = True

                        #Start the capture from a webcam
                        case 'startwebcam' :
                            webcam_index = gui_values['video-camport'] 
                            print("Starting webcam : {}".format(webcam_index))
                            video = Video(webcam_index, None, calibration_value, calibration_unit, calibration_distance)

                            #Set the video resolution (720p by default)
                            video.set_resolution(tuple(map(int, gui_values['video-resolution'].split('x'))))
                            
                            #Read the first frame
                            ret, frame = video.read()

                            #Create and resize a window and add the mouse callback (only if Show video is ticked) 
                            if gui_values['video-show']:
                                cv2.namedWindow('Frame', cv2.WINDOW_NORMAL)
                                cv2.resizeWindow('Frame', 1280, 720)
                                cv2.setMouseCallback('Frame', mouse_callback)

                            video.defined = True
                        
                        #Move the video to a specific frame (defined from the progress bar from the GUI)
                        case 'progress' :
                            #Find the frame number from the % of the video
                            video.framenum = int((video.totframe/100)*int(gui_values['video-progress']))
                            video.set_frame(video.framenum)

                        #Show/hide the OpenCV window
                        case 'show':
                            if gui_values['video-show']:
                                #Create/Display the window
                                cv2.namedWindow('Frame', cv2.WINDOW_NORMAL)
                                cv2.resizeWindow('Frame', 1280, 720)
                                cv2.setMouseCallback('Frame', mouse_callback)
                            else :
                                cv2.destroyAllWindows()

                case 'demo':
                    demo.blur = int(gui_values['demo-blur'])
                    demo.thresh1 = int(gui_values['demo-thresh1'])
                    demo.thresh2 = int(gui_values['demo-thresh2'])

                case 'plot' :
                    match eventsplit[1] :
                        case 'plot' :
                            to_gui_list.append(('W1','plot-enable', True))
                            figure = plotgui.demo_plot('Demo', [10,20])
                            to_plot.put(figure)
            #Handle GUI events-------------------------------------------------------------------------
        
        #Communicate with the GUI process to update the GUI          
        if len(to_gui_list)>0 and not to_gui.full() :
            to_gui.put(to_gui_list)
        
        #Clear the GUI envent and updates
        to_gui_list = []
        gui_event = 'none'
    #GUI-----------------------------------------------------------------------------------

    #EXIT------------------
    video.stop()
    cv2.destroyAllWindows()
    #EXIT------------------
#MAIN =====================================================================================

