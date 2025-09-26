from Telemetry.graphs.plot_ratio import create_ratio_plot

def get_sample_ratio_plots(rowers_data):
    plots = []
    for sample in range(0,8):
        sample_values = []
        for rower in rowers_data:
            data = rower['telemetry']
            values = [
                data['recovery_time_1'][sample],
                20, # Spacer
                data['recovery_time_2'][sample],
                20, # Spacer
                data['recovery_time_3'][sample],
                20, # Spacer
                data['recovery_time_4'][sample],
                data['hang_time_1'][sample],
                20, # Spacer
                data['hang_time_2'][sample], 
                data['catch_slip_time'][sample],
                data['drive_time_1'][sample],
                20, # Spacer
                data['drive_time_2'][sample],
                20, # Spacer
                data['drive_time_3'][sample],
                20, # Spacer
                data['drive_time_4'][sample],
                data['finish_slip_time'][sample],
                data['pause_time_1'][sample],
                20, # Spacer
                data['pause_time_2'][sample],
                data['recovery_time_5'][sample]
            ]
            sample_values.append(values)
        plot = create_ratio_plot(sample_values)
        plots.append(plot)
    
    return plots