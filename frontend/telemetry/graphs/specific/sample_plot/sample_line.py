from telemetry.graphs.plot_line import plot_line
from telemetry.modules.sorting import average_Array_into_One_Percentage as aaiop
from telemetry.modules.maths import calculate_Average

def get_sample_line_plots(session_data, athlete_data, x_axis_values, y_axis_values, title, x_label, y_label, percentage_x=False, percentage_y=False, names=None, pdf=False, sample=False, highlight_Effective=False):
    plots = []
    content_of_container = ''
    is_athlete_data = False
    if y_axis_values in session_data:
        content_of_container = 'boat_data'
        is_athlete_data = False
    else:
        content_of_container = 'telemetry'
        is_athlete_data = True

    if content_of_container == 'telemetry':
        graphs_Created = 0
        def loop(sample_position):
            new_x_axis_values = []
            new_y_axis_values = []
            optional_values = []

            catchnormalized = False
            finishnormalized = False

            for rower in athlete_data:
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

                if highlight_Effective:
                    gate_force_list = telem_dict['gate_force_x'][sample_position]
                    optional_values.append(gate_force_list)

            if x_label == 'Normalized Time (%)':
                catchnormalized = session_data['normalizedcatch']
                finishnormalized = session_data['normalizedfinish']
                
            plot = plot_line(new_x_axis_values, new_y_axis_values, title, x_label, y_label, names, pdf, optional_values, catchnormalized, finishnormalized, is_athlete_data, graph_Order=graphs_Created, highlight_Effective=highlight_Effective)
            return plot
        
        if type(sample) == int:
            return loop(sample)
        else:
            for i in range(0, 7):
                plots.append(loop(i))
                graphs_Created += 1
            return plots

    else:
        new_x_axis_values = []
        new_y_axis_values = []

        catchnormalized = False
        finishnormalized = False

        for sample in range(0,8):
            if x_axis_values == None:
                new_x_axis_values.append(str(session_data['rating'][sample]))
            else:
                new_x_axis_values.append(session_data[x_axis_values][sample])

            new_y_axis_values.append(session_data[y_axis_values][sample])

        if x_label == 'Normalized Time (%)':
            catchnormalized = calculate_Average(session_data['normalizedcatch'])
            finishnormalized = calculate_Average(session_data['normalizedfinish'])

        plot = plot_line(new_x_axis_values, new_y_axis_values, title, x_label, y_label, names, pdf, False, catchnormalized, finishnormalized, is_athlete_data)
        return plot