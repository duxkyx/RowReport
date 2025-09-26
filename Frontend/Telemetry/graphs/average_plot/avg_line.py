from Telemetry.graphs.plot_line import plot_line
from Telemetry.subroutines import average_Array_into_One as aaio

def get_avg_line_plot(rowers_data, xaxis, yaxis, title, xaxis_title, yaxis_title):
    y_axis_values = []
    x_axis_values = []
    for rower in rowers_data:
        data = rower['telemetry']
        y_axis_values.append(aaio(data[yaxis]))

        if type(xaxis) is list:
            x_axis_values.append(aaio(xaxis))
        else:
            x_axis_values.append(aaio(data[xaxis]))

    plot = plot_line(y_axis_values, x_axis_values, title, yaxis_title, xaxis_title)
    return plot