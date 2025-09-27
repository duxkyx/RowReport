# Returns the plot for individual user syncronisation plot
import plotly.graph_objs as go
import plotly.io as pio
from Telemetry.colours import seat_colours
from Telemetry.subroutines import is_2d_list

def create_syncronisation_plot(values, names=None):
    categories = [
        "25 Recov", "50 Recov", "75 Recov", "Hang Start",
        "Min Angle", "Catch", "Effect Start", "70 Max",
        "Max F", "Max 70", "Effect End", "Finish",
        "Max Angle", "Release"
    ]

    # Plotly radar chart
    fig = go.Figure()

    if is_2d_list(values):
        colours = list(seat_colours.values())
        iterations = 0
        for x in values:
            if names:
                name_value=f'{iterations + 1} | {names[iterations]}'
            else:
                name_value=f'{iterations + 1} | Seat'

            fig.add_trace(go.Scatterpolar(
                r=x + [x[0]],  # close the loop
                theta=categories + [categories[0]],
                fill=None,
                name=name_value,
                line=dict(color=colours[iterations])
            ))
            iterations += 1

    else:
        fig.add_trace(go.Scatterpolar(
            r=values + [values[0]],  # close the loop
            theta=categories + [categories[0]],
            fill=None,
            name='Performance'
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[-200, 100]),
            angularaxis=dict(direction="clockwise"),
        ),
        title='Syncronisation (ms)',
        autosize=True,
        showlegend=True,
        xaxis=dict(
            gridcolor='darkblue',  # Dark navy grid
        ),
        font=dict(
            color='grey'  # Default font color for text elements like legend
        ),
        paper_bgcolor="rgba(0,0,0,0)",   # outer area
        plot_bgcolor='rgba(0,0,0,0)'  # Transparent paper background
    )

    # Get HTML representation (without full page)
    graph_html = pio.to_html(
        fig,
        full_html=False,
        include_plotlyjs='cdn',
        config={
            "responsive": True, 
            "displayModeBar": False
        }
    )
    return graph_html
