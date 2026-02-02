from telemetry.graphs.plot_syncronisation import create_syncronisation_plot
from telemetry.modules.maths import calculate_Average as ca

def get_avg_syncronisation_plot(rowers_data, names, pdf=False):
    rower_syncronisation_array = []
    for rower in rowers_data:
        values = {
            "25 Recov": ca(rower['telemetry']['difference_25']),
            "50 Recov": ca(rower['telemetry']['difference_50']),
            "75 Recov": ca(rower['telemetry']['difference_75']),
            "Hang Start": ca(rower['telemetry']['difference_hang']),
            "Min Angle": ca(rower['telemetry']['difference_min']),
            "Catch": ca(rower['telemetry']['difference_catch']), 
            "Effect Start": ca(rower['telemetry']['difference_effective_start']),
            "70 Max": ca(rower['telemetry']['difference_70max']),
            "Max F": ca(rower['telemetry']['difference_maxf']),
            "Max 70": ca(rower['telemetry']['difference_max70']),
            "Effect End": ca(rower['telemetry']['difference_effective_end']),
            "Finish": ca(rower['telemetry']['difference_finish']),
            "Max Angle": ca(rower['telemetry']['difference_max']),
            "Release": ca(rower['telemetry']['difference_recovery'])
        }
        rower_syncronisation_array.append(list(values.values()))

    plot = create_syncronisation_plot(rower_syncronisation_array, names, pdf)
    return plot