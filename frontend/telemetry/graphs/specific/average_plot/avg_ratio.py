from telemetry.graphs.plot_ratio import create_ratio_plot
from telemetry.modules.maths import calculate_Average as avg

def get_avg_ratio_plot(rowers_data, names, pdf=False):
    rower_values = []
    for rower in rowers_data:
        data = rower['telemetry']
        values = [
            avg(data['recovery_time_1']),
            10, # Spacer
            avg(data['recovery_time_2']),
            10, # Spacer
            avg(data['recovery_time_3']),
            10, # Spacer
            avg(data['recovery_time_4']),
            avg(data['hang_time_1']),
            10, # Spacer
            avg(data['hang_time_2']), 
            avg(data['catch_slip_time']),
            avg(data['drive_time_1']),
            10, # Spacer
            avg(data['drive_time_2']),
            10, # Spacer
            avg(data['drive_time_3']),
            10, # Spacer
            avg(data['drive_time_4']),
            avg(data['finish_slip_time']),
            avg(data['pause_time_1']),
            10, # Spacer
            avg(data['pause_time_2']),
            avg(data['recovery_time_5'])
        ]
        rower_values.append(values)
    plot = create_ratio_plot(rower_values, names, pdf)
    
    return plot