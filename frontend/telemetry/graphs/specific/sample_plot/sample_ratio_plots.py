from telemetry.graphs.plot_ratio import create_ratio_plot

def get_sample_ratio_plots(rowers_data, names, sample):
    rower_values = []
    for rower in rowers_data:
        data = rower['telemetry']
        values = [
            data['recovery_time_1'][sample],
            10, # Spacer
            data['recovery_time_2'][sample],
            10, # Spacer
            data['recovery_time_3'][sample],
            10, # Spacer
            data['recovery_time_4'][sample],
            data['hang_time_1'][sample],
            10, # Spacer
            data['hang_time_2'][sample], 
            data['catch_slip_time'][sample],
            data['drive_time_1'][sample],
            10, # Spacer
            data['drive_time_2'][sample],
            10, # Spacer
            data['drive_time_3'][sample],
            10, # Spacer
            data['drive_time_4'][sample],
            data['finish_slip_time'][sample],
            data['pause_time_1'][sample],
            10, # Spacer
            data['pause_time_2'][sample],
            data['recovery_time_5'][sample]
        ]
        rower_values.append(values)
    plot = create_ratio_plot(rower_values, names)
    
    return plot