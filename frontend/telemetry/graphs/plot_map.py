import plotly.express as px
import plotly.io as pio
import pandas as pd
from telemetry.graphs.colours import sample_colours

def plot_map(session_data, individual_sample=None, pdf=False):
    gps = session_data['gps']    
    
    distance = round(session_data['distance'])
    total_points = sum(len(section) for section in gps)    
    rows = []
    highlighted_rows = []
    counted_points = 0

    for section_index, section in enumerate(gps, start=1):
        for point_index, (lon, lat) in enumerate(section):
            current_distance = round((distance / total_points) * (counted_points))

            if individual_sample:
                if section_index == individual_sample:
                    highlighted_rows.append({"lon": lon, "lat": lat})
                    colour = "#841925"
                else:
                    colour = '#d3d3d3'
            else:
                colour = sample_colours.get(str(section_index), '#888')


            rows.append({
                "lon": lon,
                "lat": lat,
                "section": str(section_index),
                "distance": f"{current_distance} | {distance} m",
                "point": counted_points,
                "color": colour
            })
            counted_points += 1


    coordinates_df = pd.DataFrame(rows)
    highlighted_rows = pd.DataFrame(highlighted_rows)


    # Use scatter_mapbox to allow color gradient
    fig = px.scatter_mapbox(
        coordinates_df,
        lat="lat",
        lon="lon",
        hover_name="section",
        color="color",
        hover_data={"point": True, "distance": True, "lat": True, "lon": True},
        color_discrete_map="identity",
        size_max=10,
        zoom=15,
        height=600,
    )

    # Connect points with lines
    fig.update_traces(
        mode="lines+markers",
        marker=dict(
            size=6,
            opacity=0.8,
        ),
        line=dict(
            width=3,
        )
    )
    
    # Layout
    fig.update_layout(
        showlegend=False if pdf else True,
        mapbox_style="carto-positron",
        mapbox_center={"lat": coordinates_df['lat'].mean(), "lon": coordinates_df['lon'].mean()} if not individual_sample else {"lat": highlighted_rows['lat'].mean(), "lon": highlighted_rows["lon"].mean()},
        margin={"r":0,"t":0,"l":0,"b":0},
        coloraxis_showscale=False,
        legend_title_text="Section"
    )

    if pdf:
        return fig
    else:
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