#!/usr/bin/env python

import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2Tk

sg.theme('DarkGrey9')

#Right clic menu
right_click_menu_def = [[], []]

window2 = None
newevent = None

class Toolbar(NavigationToolbar2Tk):
    def __init__(self, *args, **kwargs):
        super(Toolbar, self).__init__(*args, **kwargs)

def on_click(event):
    global newevent
    newevent = event.xdata

#Window 2 for plot=========================================================
def make_plot_window():
    plot_layout = [
        [sg.Canvas(key='plot-canvas',expand_x=True, expand_y=True)],
        [sg.Canvas(key='plot-control')],
        ]
    window = sg.Window(
        'Plot',
        plot_layout,
        right_click_menu=right_click_menu_def, 
        right_click_menu_tearoff=True, 
        grab_anywhere=False, 
        resizable=True, 
        margins=(0,0), 
        use_custom_titlebar=False, 
        finalize=False, 
        keep_on_top=True, 
        return_keyboard_events=True,
        alpha_channel=1,
    )
    return window
#Window 2 for plot=========================================================

#Draw plot to window 2=====================================================
def draw_figure_GUI(canvas, figure, toolbar):
    if canvas.children:
        for child in canvas.winfo_children():
            child.destroy()
    if toolbar.children:
        for child in toolbar.winfo_children():
            child.destroy()
    
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas) 
    figure_canvas_agg.draw()

    toolbar = Toolbar(figure_canvas_agg, toolbar)
    toolbar.update()

    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)

    figure.canvas.mpl_connect('button_press_event', on_click)

    return figure_canvas_agg
#Draw plot to window 2=====================================================


#GUI process=========================================
def gui(windows, from_gui, to_gui, to_plot):
    global newevent
    event, values = '',''
    window1, window2 = windows
    fig_agg = None

    while True :  
        #Send plot events to main (clic, keypress, ...)-
        if newevent :
            from_gui.put(('CANVAS', 'none', newevent))
            newevent = None
            continue
        #Send plot events to main (clic, keypress, ...)-

        #Send events to the GUI queue----------------
        event, values = window1.read(timeout=10)
        from_gui.put(('W1',event,values))
        #Send events to the GUI queue----------------

        #Enable/Disable plot window------------------
        if values and values['plot-enable'] :
            if window2 is None :
                window2 = make_plot_window()

            event, values = window2.read(timeout=10)
            from_gui.put(('W2',event,values))

            if event in (None, 'Exit'):
                window1['plot-enable'].update(False)
                continue
            
            #Update plot..............................
            if not to_plot.empty() :
                if fig_agg :
                    fig_agg.get_tk_widget().forget()
                figure  = to_plot.get_nowait()
                fig_agg = draw_figure_GUI(window2['plot-canvas'].TKCanvas, figure,window2['plot-control'].TKCanvas)
            #Update plot..............................

        else :
            if window2 :
                window2.close()
                window2 = None    
        #Enable/Disable plot window------------------

        #Get events from the GUI queue---------------
        if not to_gui.empty() :
            updates  = to_gui.get_nowait()

            for update in updates :
                if update[0] == 'W1' :
                    window1[update[1]].update(update[2])
                if update[0] == 'W2' :
                    if window2 is None :
                        window2 = make_plot_window()
                        window2.read(timeout=10)
                    window2[update[1]].update(update[2])
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
        sg.Checkbox('Show plot', key='plot-enable', default=False, enable_events = True),
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

#Plot tab (Tab 3)===================================================
plot_layout = [
    [sg.Button('Demo Plot', key='plot-plot')]
]
#Plot tab (Tab 3)===================================================

#GUI LAYOUT=========================================================
layout = [ 
    [sg.MenubarCustom(menu_def, key='-MENU-', font='Courier 15', tearoff=True)],
    top_layout,
    [
    sg.TabGroup([[
        sg.Tab('Video', video_layout),
        sg.Tab('Demo', demo_layout),
        sg.Tab('Plot', plot_layout)
        #You can add other tabs_layouts here 
        ]
    ],key='-TAB GROUP-', expand_x=True, expand_y=True)
    ]
    ]
#GUI LAYOUT=========================================================

#Windows creation
window1 = sg.Window('OpenCV Demo', layout ,right_click_menu=right_click_menu_def, right_click_menu_tearoff=True, grab_anywhere=True, resizable=True, margins=(0,0), use_custom_titlebar=False, finalize=False, keep_on_top=True, return_keyboard_events=True)
