import plotly.express as px
import plotly.io as pio
import pandas as pd

def plot_map(boat_data):
    coordinates = boat_data['gps']    
    coordinates_df = pd.DataFrame(coordinates, columns=['lon', 'lat'])
    coordinates_df['sections'] = [i for i in range(len(coordinates_df))]  # For coloring along path
    
    print(boat_data['tstrokes'])
    # Use scatter_mapbox to allow color gradient
    fig = px.scatter_mapbox(
        coordinates_df,
        lat="lat",
        lon="lon",
        color="sections",
        hover_name="sections",
        hover_data={"lat": True, "lon": True},
        color_continuous_scale="Turbo",   # Gradient color
        size_max=10,
        zoom=15,
        height=600
    )

    # Connect points with lines
    fig.update_traces(
        mode="lines+markers",
        marker=dict(
            size=6,
            opacity=0.8
        ),
        line=dict(
            width=3,
            color="white"  # or pick a color you like
        )
    )
    
    # Layout
    fig.update_layout(
        mapbox_style="carto-positron",
        mapbox_center={"lat": coordinates_df['lat'].mean(),
                       "lon": coordinates_df['lon'].mean()},
        margin={"r":0,"t":0,"l":0,"b":0},
        coloraxis_showscale=False
    )

    return pio.to_html(
        fig,
        full_html=False,
        include_plotlyjs='cdn',
        config={
            "responsive": True,
            "displayModeBar": True,
            "scrollZoom": True
        }
    )