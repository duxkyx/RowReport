from telemetry.graphs.plot_line import plot_line
from telemetry.modules.sorting import average_Array_into_One_Percentage as aaiop

def get_sample_line_plots(data_container, x_axis_values, y_axis_values, title, x_label, y_label, percentage_x=False, percentage_y=False, names=None, pdf=False, sample=False):
    plots = []
    content_of_container = ''
    if isinstance(data_container, dict): # Checks how the data is structured (dict within dict or just dict)
        content_of_container = 'boat_data'
    else:
        content_of_container = 'telemetry'

    if content_of_container == 'telemetry':
        def loop(sample_position):
            new_x_axis_values = []
            new_y_axis_values = []
            optional_values = []

            for rower in data_container:
                telem_dict = rower['telemetry']

                if percentage_x:
                    if type(x_axis_values) is list:
                        new_x_axis_values.append(aaiop(x_axis_values))
                    else:
                        new_x_axis_values.append(aaiop(telem_dict[x_axis_values]))
                else:
                    if type(x_axis_values) is list:
                        new_x_axis_values.append(x_axis_values[sample_position])
                    else:
                        new_x_axis_values.append(telem_dict[x_axis_values][sample_position])

                if percentage_y:
                    new_y_axis_values.append(aaiop(telem_dict[y_axis_values]))
                else:
                    new_y_axis_values.append(telem_dict[y_axis_values][sample_position])

                if title == 'Seat Position':
                    gate_force_list = telem_dict['gate_force_x'][sample_position]
                    optional_values.append(gate_force_list)
                
            plot = plot_line(new_x_axis_values, new_y_axis_values, title, x_label, y_label, names, pdf, optional_values)
            return plot
        
        if type(sample) == int:
            return loop(sample)
        else:
            for i in range(0, 7):
                plots.append(loop(i))
            return plots

    else:
        new_x_axis_values = []
        new_y_axis_values = []

        for sample in range(0,8):
            if x_axis_values == None:
                new_x_axis_values.append(str(data_container['rating'][sample]))
            else:
                new_x_axis_values.append(data_container[x_axis_values][sample])

            new_y_axis_values.append(data_container[y_axis_values][sample])

        plot = plot_line(new_x_axis_values, new_y_axis_values, title, x_label, y_label, names, pdf)
        return plot