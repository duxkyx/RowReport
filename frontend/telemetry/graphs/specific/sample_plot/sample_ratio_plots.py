from telemetry.graphs.plot_ratio import create_ratio_plot

def get_sample_ratio_plots(rowers_data, names, sample, pdf=False):
    plots = []
    def loop(sample_position):
        rower_values = []
        for rower in rowers_data:
            data = rower['telemetry']
            values = [
                data['recovery_time_1'][sample_position],
                10, # Spacer
                data['recovery_time_2'][sample_position],
                10, # Spacer
                data['recovery_time_3'][sample_position],
                10, # Spacer
                data['recovery_time_4'][sample_position],
                data['hang_time_1'][sample_position],
                10, # Spacer
                data['hang_time_2'][sample_position], 
                data['catch_slip_time'][sample_position],
                data['drive_time_1'][sample_position],
                10, # Spacer
                data['drive_time_2'][sample_position],
                10, # Spacer
                data['drive_time_3'][sample_position],
                10, # Spacer
                data['drive_time_4'][sample_position],
                data['finish_slip_time'][sample_position],
                data['pause_time_1'][sample_position],
                10, # Spacer
                data['pause_time_2'][sample_position],
                data['recovery_time_5'][sample_position]
            ]
            rower_values.append(values)

        plot = create_ratio_plot(rower_values, names, pdf)
        return plot

    if type(sample) == int:
        return loop(sample)
    else:
        for i in range(0,7):
            plots.append(loop(i))
    
    return plots