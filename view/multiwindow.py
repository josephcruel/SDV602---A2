from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import view.ChartExamples as ce
import PySimpleGUI as sg
import matplotlib as plt
import inspect
plt.use('TkAgg')
"""
    Demo - 2 simultaneous windows using read_all_window

    Both windows are immediately visible.  Each window updates the other.

    Copyright 2020 PySimpleGUI.org
"""


def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


def delete_figure_agg(figure_agg):
    figure_agg.get_tk_widget().forget()
    plt.close('all')


def make_win1():

    layout = [[sg.Text('Window 1')],
              [sg.Text('Enter something to output to Window 2')],
              [sg.Input(key='-IN-', enable_events=True)],
              [sg.Text(size=(25, 1), key='-OUTPUT-')],
              [sg.Button('Reopen')],
              [sg.Button('Exit')]]
    return sg.Window('Window Title', layout, finalize=True)


def make_win2():
    figure_agg = None
    figure_w = 650
    figure_h = 650
    layout = [[sg.Text('Window 2')],

              [sg.Canvas(size=(figure_w, figure_h), key='-CANVAS-')],
              [sg.Text('Enter something to output to Window 1')],
              [sg.Input(key='-IN-', enable_events=True)],
              [sg.Text(size=(25, 1), key='-OUTPUT-')],
              [sg.Button('Exit')]]

    window2 = sg.Window('Window Title', layout, finalize=True)
    if figure_agg:
        # ** IMPORTANT ** Clean up previous drawing before drawing again
        delete_figure_agg(figure_agg)
    # call function to get the figure
    fig = ce.line_plot()
    figure_agg = draw_figure(window2['-CANVAS-'].TKCanvas, fig)
    return window2


def main():
    figure_agg = None
    window1, window2 = make_win1(), make_win2()

    window2.move(window1.current_location()[
                 0], window1.current_location()[1]+220)

    while True:             # Event Loop
        window, event, values = sg.read_all_windows()

        if window == sg.WIN_CLOSED:     # if all windows were closed
            break

        if event == sg.WIN_CLOSED or event == 'Exit':
            window.close()
            if window == window2:       # if closing win 2, mark as closed
                window2 = None
            elif window == window1:     # if closing win 1, mark as closed
                window1 = None
        elif event == 'Reopen':
            if not window2:
                window2 = make_win2()
                window2.move(window1.current_location()[
                             0], window1.current_location()[1] + 220)
        elif event == '-IN-':
            output_window = window2 if window == window1 else window1
            if output_window:           # if a valid window, then output to it
                output_window['-OUTPUT-'].update(values['-IN-'])
            else:
                window['-OUTPUT-'].update('Other window is closed')


if __name__ == '__main__':
    main()
