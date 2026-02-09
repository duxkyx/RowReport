# Samples - Sessions
from telemetry.graphs.specific.sample_plot.sample_syncronisation_plots import get_sample_syncronisation_plots
from telemetry.graphs.specific.sample_plot.sample_ratio_plots import get_sample_ratio_plots
from telemetry.graphs.specific.sample_plot.sample_line import get_sample_line_plots

# Average - Sessions
from telemetry.graphs.specific.average_plot.avg_sync import get_avg_syncronisation_plot
from telemetry.graphs.specific.average_plot.avg_ratio import get_avg_ratio_plot
from telemetry.graphs.specific.average_plot.avg_line import get_avg_line_plot

# Overview
from telemetry.graphs.plot_map import plot_map

def return_Graphs(page_name, session_data, rowing_data, name_array, request, selected_sample=None, isPdf=False):
    returned_graphs = {}

    # Overview Page
    if page_name == 'overview' or page_name == 'all':
        returned_graphs['map'] = plot_map(
            session_data=session_data,
            pdf=isPdf
        )

    # Session Page
    if page_name == 'session' or page_name == 'all':
        rates = []
        for rate in session_data['rating']:
            rates.append(rate)

        returned_graphs['acceleration'] = get_sample_line_plots(
            session_data=session_data, 
            athlete_data=rowing_data, 
            x_axis_values='normalizedtime', 
            y_axis_values='acceleration', 
            title='Boat Acceleration', 
            x_label='Normalized Time (%)', 
            y_label='Acceleration (m/s)', 
            percentage_x=False, 
            percentage_y=False, 
            names=rates,
            pdf=isPdf
        )

        returned_graphs['rowing_speed'] = get_sample_line_plots(
            session_data=session_data, 
            athlete_data=rowing_data, 
            x_axis_values=None, 
            y_axis_values='meterspersecond', 
            title='Boat Speed', 
            x_label='Samples | Rate', 
            y_label='Speed (m/s)', 
            percentage_x=False, 
            percentage_y=False, 
            names=rates,
            pdf=isPdf
        )

        returned_graphs['power_timeline'] = get_avg_line_plot(
            session_data=session_data,
            athlete_data=rowing_data, 
            x_axis_values=None, 
            y_axis_values='power_timeline', 
            title='Power Timeline', 
            x_label='Strokes', 
            y_label='Power (W)', 
            percentage_x=False, 
            percentage_y=False, 
            names=name_array,
            pdf=isPdf
        )

        returned_graphs['boat_roll'] = get_sample_line_plots(
            session_data=session_data, 
            athlete_data=rowing_data, 
            x_axis_values='normalizedtime', 
            y_axis_values='boatroll', 
            title='Boat Roll', 
            x_label='Normalized Time (%)', 
            y_label='Roll (deg)', 
            percentage_x=False, 
            percentage_y=False, 
            names=rates,
            pdf=isPdf
        )

        returned_graphs['boat_pitch'] = get_sample_line_plots(
            session_data=session_data,
            athlete_data=rowing_data, 
            x_axis_values='normalizedtime', 
            y_axis_values='boatpitch', 
            title='Boat Pitch', 
            x_label='Normalized Time (%)', 
            y_label='Pitch (deg)', 
            percentage_x=False, 
            percentage_y=False, 
            names=rates,
            pdf=isPdf
        )

        returned_graphs['boat_yaw'] = get_sample_line_plots(
            session_data=session_data, 
            athlete_data=rowing_data, 
            x_axis_values='normalizedtime', 
            y_axis_values='boatyaw', 
            title='Boat Yaw', 
            x_label='Normalized Time (%)', 
            y_label='Yaw (deg)', 
            percentage_x=False, 
            percentage_y=False, 
            names=rates,
            pdf=isPdf
        )

    # Average Page
    if page_name == 'average' or page_name == 'all':
        
        returned_graphs['syncronisation'] = get_avg_syncronisation_plot(
            rowing_data, 
            names=name_array,
            pdf=isPdf
        )

        returned_graphs['ratios'] = get_avg_ratio_plot(
            rowing_data, 
            names=name_array,
            pdf=isPdf
        )

        returned_graphs['gateforcex'] = get_avg_line_plot(
            session_data=session_data, 
            athlete_data=rowing_data, 
            x_axis_values=session_data['normalizedtime'], 
            y_axis_values='gate_force_x', 
            title='GateForceX', 
            x_label='Normalized Time (%)', 
            y_label='Gate Force X (kg)', 
            names=name_array,
            pdf=isPdf
        )

        returned_graphs['gateanglevelocity'] = get_avg_line_plot(
            session_data=session_data, 
            athlete_data=rowing_data, 
            x_axis_values=session_data['normalizedtime'], 
            y_axis_values='gate_angle_vel', 
            title='GateAngle Velocity', 
            x_label='Normalized Time (%)', 
            y_label='Gate Angle Velocity (deg)', 
            names=name_array,
            pdf=isPdf,
            highlight_Effective=True,
        )

        returned_graphs['gateforcepercent'] = get_avg_line_plot(
            session_data=session_data, 
            athlete_data=rowing_data, 
            x_axis_values='gate_angle', 
            y_axis_values='gate_force_x', 
            title='Gate Force %', 
            x_label='Drive Length (%)', 
            y_label='Gate Force (%)', 
            percentage_x=True, 
            percentage_y=True, 
            names=name_array,
            pdf=isPdf
        )

        returned_graphs['gateanglevelocitydeg'] = get_avg_line_plot(
            session_data=session_data, 
            athlete_data=rowing_data, 
            x_axis_values='gate_angle',
            y_axis_values='gate_angle_vel',
            title='GateAngle Velocity',
            x_label='GateAngle (deg)',
            y_label='Gate Angle Velocity (deg/s) ',
            percentage_x=False,
            percentage_y=False,
            names=name_array,
            pdf=isPdf
        )

        # Only generate these graphs if seat sensors are valid in the session recording.
        if session_data['seat_sensors']:
            returned_graphs['legsvelocity'] = get_avg_line_plot(
                session_data=session_data, 
                athlete_data=rowing_data, 
                x_axis_values=session_data['normalizedtime'], 
                y_axis_values='seat_posn_vel', 
                title='Legs Velocity',
                x_label='Normalized Time (%)', 
                y_label='Legs Velocity (deg/s)', 
                names=name_array,
                pdf=isPdf,
                highlight_Effective=True
            )

            returned_graphs['seatposition'] = get_avg_line_plot(
                session_data=session_data, 
                athlete_data=rowing_data, 
                x_axis_values='gate_angle', 
                y_axis_values='seat_posn', 
                title='Seat Position', 
                x_label='Gate Angle (deg)', 
                y_label='Seat Position', 
                names=name_array,
                pdf=isPdf,
                highlight_Effective=True
            )

            returned_graphs['legsvelocitygateangle'] = get_avg_line_plot(
                session_data=session_data, 
                athlete_data=rowing_data, 
                x_axis_values='gate_angle', 
                y_axis_values='seat_posn_vel', 
                title='Legs Velocity', 
                x_label='Drive Length (%)', 
                y_label='Legs Velocity (deg/s)', 
                percentage_x=True,
                percentage_y=False, 
                names=name_array,
                pdf=isPdf,
                highlight_Effective=True
            )

            returned_graphs['bodyarmsvelocity'] = get_avg_line_plot(
                session_data=session_data, 
                athlete_data=rowing_data, 
                x_axis_values='gate_angle', 
                y_axis_values='body_arms_vel', 
                title='Body + Arms Velocity', 
                x_label='Drive Length (%)', 
                y_label='Body + Arms Velocity (deg/s)', 
                percentage_x=True,
                percentage_y=False, 
                names=name_array,
                pdf=isPdf,
                highlight_Effective=True
            )

    if (request.method == 'POST' and page_name == 'samples') or page_name == 'all':
        if type(selected_sample) == int:
            selected_sample -= 1

        returned_graphs['sample_map'] = plot_map(
            session_data,
            selected_sample,
            pdf=isPdf
        )

        returned_graphs['sample_syncronisation'] = get_sample_syncronisation_plots(
            rowing_data, 
            names=name_array, 
            sample=selected_sample,
            pdf=isPdf
        )

        returned_graphs['sample_ratios'] = get_sample_ratio_plots(
            rowing_data, 
            names=name_array, 
            sample=selected_sample,
            pdf=isPdf
        )

        returned_graphs['sample_gateforcex'] = get_sample_line_plots(
            session_data=session_data, 
            athlete_data=rowing_data,  
            x_axis_values=session_data['normalizedtime'], 
            y_axis_values='gate_force_x', 
            title='GateForceX', 
            x_label='Normalized Time (%)', 
            y_label='Gate Force X (kg)', 
            names=name_array,
            sample=selected_sample,
            pdf=isPdf,
        )

        returned_graphs['sample_gateanglevelocity'] = get_sample_line_plots(
            session_data=session_data, 
            athlete_data=rowing_data, 
            x_axis_values=session_data['normalizedtime'], 
            y_axis_values='gate_angle_vel', 
            title='GateAngle Velocity', 
            x_label='Normalized Time (%)', 
            y_label='Gate Angle Velocity (deg/s)', 
            names=name_array,
            sample=selected_sample,
            pdf=isPdf,
            highlight_Effective=True,
        )

        returned_graphs['sample_gateforcepercent'] = get_sample_line_plots(
            session_data=session_data, 
            athlete_data=rowing_data, 
            x_axis_values='gate_angle', 
            y_axis_values='gate_force_x', 
            title='Gate Force %', 
            x_label='Drive Length (%)', 
            y_label='Gate Force (%)', 
            percentage_x=True, 
            percentage_y=True, 
            names=name_array,
            sample=selected_sample,
            pdf=isPdf
        )

        returned_graphs['sample_gateanglevelocitydeg'] = get_sample_line_plots(
            session_data=session_data, 
            athlete_data=rowing_data, 
            x_axis_values='gate_angle',
            y_axis_values='gate_angle_vel',
            title='GateAngle Velocity',
            x_label='GateAngle (deg)',
            y_label='Gate Angle Velocity (deg/s) ',
            percentage_x=False,
            percentage_y=False,
            names=name_array,
            sample=selected_sample,
            pdf=isPdf
        )

        if session_data['seat_sensors']:
            returned_graphs['sample_legsvelocity'] = get_sample_line_plots(
                session_data=session_data, 
                athlete_data=rowing_data, 
                x_axis_values=session_data['normalizedtime'], 
                y_axis_values='seat_posn_vel', 
                title='Legs Velocity',
                x_label='Normalized Time (%)', 
                y_label='Legs Velocity (deg)', 
                names=name_array,
                sample=selected_sample,
                pdf=isPdf,
                highlight_Effective=True,
            )

            returned_graphs['sample_seatposition'] = get_sample_line_plots(
                session_data=session_data, 
                athlete_data=rowing_data,  
                x_axis_values='gate_angle', 
                y_axis_values='seat_posn', 
                title='Seat Position', 
                x_label='Gate Angle (deg)', 
                y_label='Seat Position', 
                names=name_array,
                sample=selected_sample,
                pdf=isPdf,
                highlight_Effective=True,
            )

            returned_graphs['sample_legsvelocitygateangle'] = get_sample_line_plots(
                session_data=session_data, 
                athlete_data=rowing_data, 
                x_axis_values='gate_angle', 
                y_axis_values='seat_posn_vel', 
                title='Legs Velocity', 
                x_label='Drive Length (%)', 
                y_label='Legs Velocity', 
                percentage_x=True,
                percentage_y=False, 
                names=name_array,
                sample=selected_sample,
                pdf=isPdf,
                highlight_Effective=True,
            )

            returned_graphs['sample_bodyarmsvelocity'] = get_sample_line_plots(
                session_data=session_data, 
                athlete_data=rowing_data, 
                x_axis_values='gate_angle', 
                y_axis_values='body_arms_vel', 
                title='Body + Arms Velocity', 
                x_label='Drive Length (%)', 
                y_label='Body Arms Vel', 
                percentage_x=True,
                percentage_y=False, 
                names=name_array,
                sample=selected_sample,
                pdf=isPdf,
                highlight_Effective=True,
            )

    return returned_graphs