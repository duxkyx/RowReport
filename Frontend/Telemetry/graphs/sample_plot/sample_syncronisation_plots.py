from Telemetry.graphs.plot_syncronisation import create_syncronisation_plot

def get_sample_syncronisation_plots(rowers_data):
    plots = []
    for sample in range(0,8):
        sample_values = []
        for rower in rowers_data:
            values = {
                "25 Recov": rower['telemetry']['difference_25'][sample],
                "50 Recov": rower['telemetry']['difference_50'][sample],
                "75 Recov": rower['telemetry']['difference_75'][sample],
                "Hang Start": rower['telemetry']['difference_hang'][sample],
                "Min Angle": rower['telemetry']['difference_min'][sample],
                "Catch": rower['telemetry']['difference_catch'][sample], 
                "Effect Start": rower['telemetry']['difference_effective_start'][sample],
                "70 Max": rower['telemetry']['difference_70max'][sample],
                "Max F": rower['telemetry']['difference_maxf'][sample],
                "Max 70": rower['telemetry']['difference_max70'][sample],
                "Effect End": rower['telemetry']['difference_effective_end'][sample],
                "Finish": rower['telemetry']['difference_finish'][sample],
                "Max Angle": rower['telemetry']['difference_max'][sample],
                "Release": rower['telemetry']['difference_recovery'][sample]
            }
            sample_values.append(list(values.values()))
        plot = create_syncronisation_plot(sample_values)
        plots.append(plot)
    
    return plots