from Telemetry.graphs.plot_ratio import create_ratio_plot
from Telemetry.subroutines import calculate_Average as ca

def get_avg_ratio_plot(rowers_data, names):
    sample_values = []
    for rower in rowers_data:
        data = rower['telemetry']
        values = [
            ca(data['recovery_time_1']),
            10, # Spacer
            ca(data['recovery_time_2']),
            10, # Spacer
            ca(data['recovery_time_3']),
            10, # Spacer
            ca(data['recovery_time_4']),
            ca(data['hang_time_1']),
            10, # Spacer
            ca(data['hang_time_2']), 
            ca(data['catch_slip_time']),
            ca(data['drive_time_1']),
            10, # Spacer
            ca(data['drive_time_2']),
            10, # Spacer
            ca(data['drive_time_3']),
            10, # Spacer
            ca(data['drive_time_4']),
            ca(data['finish_slip_time']),
            ca(data['pause_time_1']),
            10, # Spacer
            ca(data['pause_time_2']),
            ca(data['recovery_time_5'])
        ]
        sample_values.append(values)
    plot = create_ratio_plot(sample_values, names)
    
    return plot