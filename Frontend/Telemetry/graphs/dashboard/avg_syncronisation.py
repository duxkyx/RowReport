# Returns the plot for individual user syncronisation plot
import plotly.graph_objs as go
import plotly.io as pio
from Telemetry.api_requests.get_radar_averages import get_radar_averages
from Telemetry.graphs.plot_syncronisation import create_syncronisation_plot

def get_avg_syncronisation_dashboard(user_id):
    data = get_radar_averages(user_id)
    if data:
        array = [list(data['UT1'].values()), list(data['UT2'].values())]
        plot = create_syncronisation_plot(array, ['UT1', 'UT2'])
        return plot