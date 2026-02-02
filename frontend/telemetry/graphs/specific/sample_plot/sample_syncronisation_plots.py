from telemetry.graphs.plot_syncronisation import create_syncronisation_plot

def get_sample_syncronisation_plots(rowers_data, names, sample, pdf=False):
    plots = []
    def loop(sample_position):
        rower_syncronisation_array = []
        for rower in rowers_data:
            values = {
                "25 Recov": rower['telemetry']['difference_25'][sample_position],
                "50 Recov": rower['telemetry']['difference_50'][sample_position],
                "75 Recov": rower['telemetry']['difference_75'][sample_position],
                "Hang Start": rower['telemetry']['difference_hang'][sample_position],
                "Min Angle": rower['telemetry']['difference_min'][sample_position],
                "Catch": rower['telemetry']['difference_catch'][sample_position], 
                "Effect Start": rower['telemetry']['difference_effective_start'][sample_position],
                "70 Max": rower['telemetry']['difference_70max'][sample_position],
                "Max F": rower['telemetry']['difference_maxf'][sample_position],
                "Max 70": rower['telemetry']['difference_max70'][sample_position],
                "Effect End": rower['telemetry']['difference_effective_end'][sample_position],
                "Finish": rower['telemetry']['difference_finish'][sample_position],
                "Max Angle": rower['telemetry']['difference_max'][sample_position],
                "Release": rower['telemetry']['difference_recovery'][sample_position]
            }
            rower_syncronisation_array.append(list(values.values()))

        plot = create_syncronisation_plot(rower_syncronisation_array, names, pdf)
        return plot
    
    if type(sample) == int:
        return loop(sample)
    else:
        for i in range(0,7):
            plots.append(loop(i))

    return plots