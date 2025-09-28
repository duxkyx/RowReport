from Telemetry.graphs.plot_line import plot_line
from Telemetry.subroutines import average_Array_into_One_Percentage as aaiop

def get_sample_line_plots(data_container, xaxis, yaxis, title, xaxis_title, yaxis_title, percentage_x=False, percentage_y=False, names=None):
    plots = []
    content_of_container = ''
    if isinstance(data_container, dict): # Checks how the data is structured (dict within dict or just dict)
        content_of_container = 'boat_data'
    else:
        content_of_container = 'telemetry'

    if content_of_container == 'telemetry':
        for sample in range(0,8):
            y_axis_values = []
            x_axis_values = []

            for rower in data_container:
                telem_dict = rower['telemetry']
    
                if percentage_x:
                    if type(xaxis) is list:
                        x_axis_values.append(aaiop(xaxis))
                    else:
                        x_axis_values.append(aaiop(telem_dict[xaxis]))
                else:
                    if type(xaxis) is list:
                        x_axis_values.append(xaxis[sample])
                    else:
                        x_axis_values.append(telem_dict[xaxis][sample])

                if percentage_y:
                    y_axis_values.append(aaiop(telem_dict[yaxis]))
                else:
                    y_axis_values.append(telem_dict[yaxis][sample])
            
            plot = plot_line(y_axis_values, x_axis_values, title, yaxis_title, xaxis_title, names)
            plots.append(plot)

    else:
        y_axis_values = []
        x_axis_values = []

        for sample in range(0,8):
            if xaxis == None:
                x_axis_values.append(str(data_container['rating'][sample]))
            else:
                x_axis_values.append(data_container[xaxis][sample])

            y_axis_values.append(data_container[yaxis][sample])

        plot = plot_line(y_axis_values, x_axis_values, title, yaxis_title, xaxis_title, names)
        return plot
    
    return plots