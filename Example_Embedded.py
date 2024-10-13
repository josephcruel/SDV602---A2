"""
Presents an example based on Demo_Matplotlib_Browser
"""
import ChartExamples as ce 

import PySimpleGUI as sg
import matplotlib
import inspect
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import numpy as np
import matplotlib.pyplot as plt

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

def delete_figure_agg(figure_agg):
    figure_agg.get_tk_widget().forget()
    plt.close('all')

def embedded_plt(fig_dict):
    sg.theme('LightGreen')

    figure_w, figure_h = 650, 650
    # define the form layout
    listbox_values = list(fig_dict)
    col_listbox = [[sg.Listbox(values=listbox_values, enable_events=True, size=(28, len(listbox_values)), key='-LISTBOX-')],
                [sg.Text(' ' * 12), sg.Exit(size=(5, 2))]]

    layout = [[sg.Text('Matplotlib Plot Test', font=('current 18'))],
            [sg.Col(col_listbox, pad=(5, (3, 330))), sg.Canvas(size=(figure_w, figure_h), key='-CANVAS-') ,
            sg.MLine(size=(70, 35), pad=(5, (3, 90)), key='-MULTILINE-')],]

    # create the form and show it without the plot
    window = sg.Window('Our Demo Application - Embedding Matplotlib In PySimpleGUI with **kwargs', layout, grab_anywhere=False, finalize=True)
    figure_agg = None
    # The GUI Event Loop
    while True:
        event, values = window.read()
        # print(event, values)                  # helps greatly when debugging
        if event in (sg.WIN_CLOSED, 'Exit'):             # if user closed window or clicked Exit button
            break
        if figure_agg:
            # ** IMPORTANT ** Clean up previous drawing before drawing again
            delete_figure_agg(figure_agg)
        choice = values['-LISTBOX-'][0]                 # get first listbox item chosen (returned as a list)
        func_tuple = fig_dict[choice]                         # get function to call from the dictionary
        kwargs = func_tuple[1]
        func = func_tuple[0]
        window['-MULTILINE-'].update(inspect.getsource(func))  # show source code to function in multiline
        
        fig = func(**kwargs)                                    # call function to get the figure
        figure_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig)  # draw the figure
    window.close()

if __name__ == "__main__":
    #ce.show_figFunc(ce.bar_chart)

    dictionary_of_figure_functions = {'Line Plot':(ce.line_plot,{}),'Plot Dots(discrete plot)':(ce.discrete_plot,{}),
    'Name and Label':(ce.names_labels,{}),'Plot many Lines':(ce.multiple_plots,{}),
    'Bar Chart':(ce.bar_chart,{}),'Histogram':(ce.histogram,{'title':'Our Histogram Name'}),
    'Scatter Plots':(ce.scatter_plots,{}),'Stack Plot':(ce.stack_plot,{}),
    'Pie Chart 1':(ce.pie_chart1,{}),
    'Pie Chart 2':(ce.pie_chart2,{})}
    embedded_plt(dictionary_of_figure_functions)