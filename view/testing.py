import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Function to draw a matplotlib figure onto a PySimpleGUI canvas
def draw_figure(canvas, figure):
    """
    Draw a matplotlib figure onto a PySimpleGUI canvas
    """
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

# The bar chart function - got from ChartExamples.py
def bar_chart():
    """
    A bar chart showing the number of visitors 
    """
    years = [str(year) for year in range(2010, 2021)]
    visitors = [1241, 50927, 162242, 222093, 
                665004, 2071987, 2460407, 3799215, 
                5399000, 5474016, 6003672]
    plt.figure()  
    plt.bar(years, visitors, color="green")
    plt.xlabel("Years")
    plt.ylabel("Values")
    plt.title("Bar Chart Example")
    
    return plt.gcf()  

# The line plot function - got from ChartExamples.py
def line_plot():
    """
    A line plot that have set points.
    """
    plt.figure()  
    plt.plot([-1, -4.5, 16, 23])
    plt.title("Line Chart Example")
     
    return plt.gcf()

# The pie chart function - got from ChartExamples.py
def pie_chart1():
    """
    A pie chart with different programming languages.
    """
    labels = 'C', 'Python', 'Java', 'C++', 'C#'
    sizes = [13.38, 11.87, 11.74, 7.81, 4.41]
    explode = (0, 0.1, 0, 0, 0)  # only "explode" the 2nd slice (i.e. 'Python')

    plt.figure()  # Create a new figure
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=0)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.title('TIOBE Index for May 2021')
    
    return plt.gcf()

# Function to create the window layout with a chart placeholder
def create_window(des_name):
    """
    Main function that sets up the Data Explorer Screens (DES) and handles window navigation.
    """
    
    # Chart and buttons are on the left side of the window
    left_display = [
        [sg.Text(f"{des_name} - Data Explorer Screen", font=("Helvetica", 16))],
        [sg.Canvas(size=(400, 300), key='-CANVAS-')],  # Chart canvas placeholder
        [sg.Button('Set Data Source'), sg.Button('Upload Data Source')],
        [sg.Button('Pan'), sg.Button('+/-'), sg.Button('Next'), sg.Button('Exit')]
    ]

    # Chat is on the right side of the window
    right_display = [
        [sg.Text('Chat', font=("Helvetica", 16))],
        [sg.Multiline(size=(30, 30), key='-CHAT-', disabled=True)],  # Chat log
        [sg.InputText(size=(30, 1), key='-CHAT_INPUT-')],
        [sg.Button('Send Chat')]
    ]

    # Putting the left and right displays side by side
    layout = [
        [sg.Column(left_display), sg.Column(right_display)]
    ]
    
    # Return the window
    return sg.Window(des_name, layout, finalize=True) 

# Main function with the bar chart displayed as a placeholder
def main():
    
    # Create windows for each DES screen
    windows = {
        "DES 1": create_window("DES 1"),
        "DES 2": create_window("DES 2"),
        "DES 3": create_window("DES 3"),
    }

    # Create the bar chart to display in the first window (DES 1)
    figure_agg1 = draw_figure(
        windows["DES 1"]['-CANVAS-'].TKCanvas, 
        bar_chart()
    )  # Bar chart for DES 1
    figure_agg2 = draw_figure(
        windows["DES 2"]['-CANVAS-'].TKCanvas, 
        pie_chart1()
    )  # Pie chart for DES 2
    figure_agg3 = draw_figure(
        windows["DES 3"]['-CANVAS-'].TKCanvas,
        line_plot()
    )  # Line chart for DES 3

    # Hide all windows except the first 
    windows["DES 2"].hide()
    windows["DES 3"].hide()

    current_window = windows["DES 1"]
    des_order = ["DES 1", "DES 2", "DES 3"]
    current_index = 0  # Shows the first window

    chat_log = ""  # Store chat messages

    while True:
        event, values = current_window.read()

        if event == sg.WIN_CLOSED or event == 'Exit':
            break  # Exit the window

        # Move to next DES window
        if event == 'Next':
            current_window.hide()  # Hide the current window
            current_index = (
                current_index + 1
            ) % len(des_order)  # Move to the next window, DES 3 will return back to DES 1
            current_window = windows[des_order[current_index]]
            current_window.un_hide()  # Show the next window

    # Close all windows
    for window in windows.values():
        window.close()

if __name__ == "__main__":
    main()
