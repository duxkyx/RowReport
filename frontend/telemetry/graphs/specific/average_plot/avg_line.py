from telemetry.graphs.plot_line import plot_line
from telemetry.modules.sorting import average_Array_into_One as aaio
from telemetry.modules.sorting import average_Array_into_One_Percentage as aaiop
from telemetry.modules.maths import calculate_Average

def get_avg_line_plot(session_data, athlete_data, x_axis_values, y_axis_values, title, x_label, y_label, percentage_x=False, percentage_y=False, names=None, pdf=False):
    new_x_axis_values = []
    new_y_axis_values = []
    optional_values = []
    catchnormalized = False
    finishnormalized = False
    for rower in athlete_data:
        data = rower['telemetry']

        # Checks if the plot requires averages or is it just plain plotting of values. (power_timeline)
        if x_axis_values != None:
            if percentage_x:
                if type(x_axis_values) is list:
                    new_x_axis_values.append(aaiop(x_axis_values))
                else:
                    new_x_axis_values.append(aaiop(data[x_axis_values]))
            else:
                if type(x_axis_values) is list:
                    new_x_axis_values.append(aaio(x_axis_values))
                else:
                    new_x_axis_values.append(aaio(data[x_axis_values]))

            if percentage_y:
                new_y_axis_values.append(aaiop(data[y_axis_values]))
            else:
                new_y_axis_values.append(aaio(data[y_axis_values]))

        else:
            new_x_axis_values.append(list(range(1, len(data[y_axis_values]) + 1)))
            new_y_axis_values.append(data[y_axis_values])

        # To create the differnet colour lines for seat position based on gateforcex
        if title == 'Seat Position':
            gate_force_list = aaio(data['gate_force_x'])
            optional_values.append(gate_force_list)

    if x_label == 'Normalized Time (%)':
        catchnormalized = calculate_Average(session_data['normalizedcatch'])
        finishnormalized = calculate_Average(session_data['normalizedfinish'])

    plot = plot_line(new_x_axis_values, new_y_axis_values, title, x_label, y_label, names, pdf, optional_values, catchnormalized, finishnormalized, athlete_data=True)
    return plot