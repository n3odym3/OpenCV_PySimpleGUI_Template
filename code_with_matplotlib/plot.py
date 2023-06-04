#!/usr/bin/env python
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, FigureCanvasAgg
from matplotlib.figure import Figure
import numpy as np
from random import randint

class PlotGUI :
	def __init__(self):
		self.figure = None
		self.axes = None
		self.control = None
		self.enabled = False
	
	def create_figure(self) :
		if self.figure :
			self.figure.clf()
		else :
			self.figure = Figure()
		self.axes = self.figure.add_subplot(111)
	
	def save_figure(self, gui_values, gui_plot_values):
		videopath = gui_values['video-folder'].split('/').pop().split('.')[0]
		path = gui_values['video-folder'][0:gui_values['video-folder'].index(videopath)]
		outfilename = path + gui_plot_values['file-figname'] + "_" + self.type + '.svg'
		self.figure.savefig(outfilename)
		print('Saving ' + outfilename)
		return
		
	def demo_plot(self,title, data):
		self.create_figure()
		x = np.arange(0, 5, 0.1)
		y = np.sin(x)
		self.axes.plot(x, y)
		self.axes.set_title(title)
		return self.figure


