#!/usr/bin/env python

import PySimpleGUI as sg

sg.theme('DarkGrey9')

#Right clic menu
right_click_menu_def = [[], []]

#GUI process=========================================
def gui(window, from_gui, to_gui):
    event, values = '',''
    while True :  
        #Send events to the GUI queue----------------
        event, values = window.read(timeout=10)
        from_gui.put((event,values))
        #Send events to the GUI queue----------------

        #Get events from the GUI queue---------------
        if not to_gui.empty() :
            updates  = to_gui.get_nowait()
            for update in updates :
                window[update[0]].update(update[1])
        #Get events from the GUI queue---------------
#GUI process=========================================

#Top menu===============================
menu_def = [['&Application', ['E&xit']]]
#Top menu===============================

#Top layout=========================================================
top_layout = [
    [   
        sg.Button('Pause', key='video-pause'),
        sg.Button('Start file', key='video-startfile'),
        sg.Text('Speed', font=('Helvetica', 10)),
        sg.Slider(key='video-speed',size=(10,10),font=('Helvetica', 8),range=(100,1),default_value=20, orientation='h',enable_events = True),
        sg.Text(key='video-curfps', text='FPS : na')
    ],     
    [   
        sg.Checkbox('Show video', key='video-show', default=True, enable_events = True),
        sg.VSep(),
        sg.Text('Progress', font=('Helvetica', 10)),
        sg.Slider(key='video-progress',size=(30,10),font=('Helvetica', 8),range=(0,100),default_value=0, orientation='h',enable_events = True)
    ]
    ]
#Top layout=========================================================

#Video tab (Tab 1)==================================================
video_layout = [
    
    [sg.Text('Video', font=('Helvetica', 10, 'bold', 'underline'))],
    [sg.FileBrowse(),sg.Text('Folder'), sg.In(size=(25,1), enable_events=True ,key='video-folder')],
    [sg.Text(key='video-info', text='Res : na FPS : na')],
    [sg.HSep()],

    [sg.Text('Webcam',font=('Helvetica', 10, 'bold', 'underline'))],
    [
        sg.Text('Cam port'), sg.Spin([i for i in range(-1,11)], initial_value=1, k='video-camport'), 
        sg.OptionMenu(values=('1920x1080', '1280x720', '640x480'), default_value = '1280x720' , k='video-resolution'),
        sg.Button('Start webcam', key='video-startwebcam')
    ],
    [sg.HSep()],

    [sg.Text('Image settings', font=('Helvetica', 10, 'bold', 'underline'))],
    [
        sg.Button('Update', key='video-updatecal'),
        sg.Text('Distance', font=('Helvetica', 10)),
        sg.InputText("100",size=(5,1),key="calibration-distance"),
        sg.InputText("px",size=(5,1),key="calibration-unit"),
        sg.Text('Value', font=('Helvetica', 10)),
        sg.InputText("1",size=(5,1),key="calibration-value"),
    ],
    [
        sg.Checkbox('Sizeref',key='video-sizeref', default=True,enable_events = True),
        sg.Checkbox('FPS',key='video-fps', default=True,enable_events = True)
    ],
    [sg.HSep()],
]
#Video tab (Tab 1)==================================================

#Demo tab (Tab 2)===================================================
demo_layout = [
    [sg.Text('Edge detection demo', font=('Helvetica', 10, 'bold', 'underline'))],
    [sg.Checkbox('Edge detection',key='demo-edge', default=False,enable_events = True)],
    [
    sg.Text('Blur', font=('Helvetica', 10)),
    sg.Slider(key='demo-blur',size=(20,10),font=('Helvetica', 8),range=(3,15),default_value=3, resolution=2, orientation='h',enable_events = True)
    ],
    [
    sg.Text('Tresh 1', font=('Helvetica', 10)),
    sg.Slider(key='demo-thresh1',size=(20,10),font=('Helvetica', 8),range=(10,250),default_value=50, resolution=10, orientation='h',enable_events = True)
    ],
    [
    sg.Text('Tresh 2', font=('Helvetica', 10)),
    sg.Slider(key='demo-thresh2',size=(20,10),font=('Helvetica', 8),range=(10,250),default_value=150, resolution=10, orientation='h',enable_events = True)
    ]
]
#Demo tab (Tab 2)===================================================

#GUI LAYOUT=========================================================
layout = [ 
    [sg.MenubarCustom(menu_def, key='-MENU-', font='Courier 15', tearoff=True)],
    top_layout,
    [
    sg.TabGroup([[
        sg.Tab('Video', video_layout),
        sg.Tab('Demo', demo_layout),
        #You can add other tabs_layouts here 
        ]
    ],key='-TAB GROUP-', expand_x=True, expand_y=True)
    ]
    ]
#GUI LAYOUT=========================================================

#Windows creation
window = sg.Window('Settings', layout ,right_click_menu=right_click_menu_def, right_click_menu_tearoff=True, grab_anywhere=True, resizable=True, margins=(0,0), use_custom_titlebar=False, finalize=False, keep_on_top=True, return_keyboard_events=True)