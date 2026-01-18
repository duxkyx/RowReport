import plotly.express as px
import plotly.io as pio
import pandas as pd

def plot_map(boat_data):
    coordinates = boat_data['gps']
    coordinates_df = pd.DataFrame(coordinates, columns=['lon', 'lat'])

    fig = px.line_mapbox(
        coordinates_df,
        lat="lat",
        lon="lon",
        zoom=15,
        height=500,
    )

    # Set the Mapbox token (optional if using open-source maps)
    fig.update_layout(
        mapbox_style="open-street-map",  # or "carto-positron", etc.
        margin={"r":0,"t":0,"l":0,"b":0}
    )
    
    return pio.to_html(fig, full_html=False, include_plotlyjs='cdn', config={
        "responsive": True,
        "displayModeBar": False
    })