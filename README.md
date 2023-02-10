

# OpenCV PySimpleGUI Template

## What is the purpose of this code ?

Starting a new OpenCV project from scratch can be time-consuming and repetitive, as everything has to be manually programmed.  From Webcam/video selection, frame reading, to images visualization, you always re-write the exact same code every time. Adjusting the parameters of the computer vision algorithm can also be a tedious task if the values are hard coded in your script, and some time seeing in real time the effect of the modifications can be very helpful. 

This template code try to address these issues by providing the minimal code required to manipulate a video file/webcam stream while simplifying the application/adjustment of video processing thanks to a graphical user interface based on PySimpleGUI. To adapt this code for your specific task, you just need to add a few lines of code to implement your desired algorithms. 

## What does the code do ?

The code is currently able to perform the following tasks :
 - Open a file brower to select a video
 - Select a webcam and change its resolution
 - Play/pause the video
 -  Change the video speed
 - Show/hide the video (to accelerate the video processing) 
 - Display a usable progress bar 
 - Calculate/display the current framerate
 - Measure distances in your preferred unit (pixels, µm, cm,...)
 
 ## Dependencies
 - [OpenCV python](https://github.com/opencv/opencv) ([Doc](https://opencv.org/))
 - [PySimpleGUI](https://github.com/PySimpleGUI) ([Doc](https://www.pysimplegui.org/en/latest/))
 
**Installation**
```pip install opencv-python```
```pip install pysimplegui```

## The GUI 
<img src="https://github.com/n3odym3/OpenCV_PySimpleGUI_Template/blob/main/img/gui.png" width="40%">

The GUI will run in a different process (using the python *multiprocessing* library) to keep it responsive even if the OpenCV analysis is CPU intensive. 
GUI event and values are passed to the main process using a queue.

The gui key does not follow the naming convention (**-NAME-**)of PySimpleGUI. Instead, i'm using a two word **group-topic** system that allows to easily differentiate and react to the various events (*see  match eventsplit[0] and match eventsplit[1] in the code*).

## Demo
As i'm working with microalgae in my lab the video displayed in the demo showcases cells of *Euglena gracilis*. However, this template can be adapted for use with any type of video. 

### Play/pause video
<img src="https://github.com/n3odym3/OpenCV_PySimpleGUI_Template/blob/main/img/play_pause_video.gif" width="40%">

### Hide/show video
<img src="https://github.com/n3odym3/OpenCV_PySimpleGUI_Template/blob/main/img/hide_show_video.gif" width="40%">

### Video speed
<img src="https://github.com/n3odym3/OpenCV_PySimpleGUI_Template/blob/main/img/progress_bar_and_fps.gif" width="40%">

### Progress bar
<img src="https://github.com/n3odym3/OpenCV_PySimpleGUI_Template/blob/main/img/progress_bar.gif" width="40%">

### Image calibration
Image calibration can be performed by observing an object of a known size and defining the **distance per pixel** constant. 

In this example, the calibration value of the 720p video of my microscope is 0.75µm/pixel which mean that one pixel on the image correspond to 0.75µm in real life. 

If you change the video resolution or the magnification (zoom) of your camera, the calibration needs to be redone ton match the new parameters.

<img src="https://github.com/n3odym3/OpenCV_PySimpleGUI_Template/blob/main/img/scale_update.gif" width="40%">

### Processing demo
<img src="https://github.com/n3odym3/OpenCV_PySimpleGUI_Template/blob/main/img/demo.gif" width="40%">
