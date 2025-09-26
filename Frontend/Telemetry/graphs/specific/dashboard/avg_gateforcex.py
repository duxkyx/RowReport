# Returns the plot for individual user syncronisation plot
import plotly.graph_objs as go
import plotly.io as pio
from Telemetry.api_requests.get_gateforce_averages import get_gateforce_averages
from Telemetry.graphs.plot_line import plot_line

def get_avg_gateforcex_dashboard(user_id):
    gate_force_data = get_gateforce_averages(user_id)
    if gate_force_data:
        yarray = [gate_force_data['UT1'], gate_force_data['UT2']]
        xarray = [gate_force_data['UT1_xaxis'], gate_force_data['UT2_xaxis']]
        plot = plot_line(
            y_array=yarray, 
            x_array=xarray, 
            title='Gate Force X',
            yaxis_title='GateForceX',
            xaxis_title='% Drive',
            names=['UT1', 'UT2']
        )
        return plot