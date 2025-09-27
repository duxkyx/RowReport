from Telemetry.graphs.plot_line import plot_line
from Telemetry.subroutines import average_Array_into_One as aaio
from Telemetry.subroutines import average_Array_into_One_Percentage as aaiop

def get_avg_line_plot(rowers_data, xaxis, yaxis, title, xaxis_title, yaxis_title, percentage_x=False, percentage_y=False, names=None):
    y_axis_values = []
    x_axis_values = []
    for rower in rowers_data:
        data = rower['telemetry']

        if percentage_x:
            if type(xaxis) is list:
                x_axis_values.append(aaiop(xaxis))
            else:
                x_axis_values.append(aaiop(data[xaxis]))
        else:
            if type(xaxis) is list:
                x_axis_values.append(aaio(xaxis))
            else:
                x_axis_values.append(aaio(data[xaxis]))

        if percentage_y:
            y_axis_values.append(aaiop(data[yaxis]))
        else:
            y_axis_values.append(aaio(data[yaxis]))


    plot = plot_line(y_axis_values, x_axis_values, title, yaxis_title, xaxis_title, names)
    return plot