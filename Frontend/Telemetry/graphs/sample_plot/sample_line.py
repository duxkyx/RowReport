from Telemetry.graphs.plot_line import plot_line

def get_sample_line_plots(rowers_data, xaxis, yaxis, title, xaxis_title, yaxis_title):
    plots = []
    for sample in range(0,8):
        y_axis_values = []
        x_axis_values = []
        for rower in rowers_data:
            data = rower['telemetry']
            y_axis_values.append(data[yaxis][sample])

            if type(xaxis) is list:
                x_axis_values.append(xaxis[sample])
            else:
                x_axis_values.append(data[xaxis][sample])

        plot = plot_line(y_axis_values, x_axis_values, title, yaxis_title, xaxis_title)
        plots.append(plot)
    
    return plots