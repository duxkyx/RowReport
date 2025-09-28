import plotly.graph_objects as go
import plotly.io as pio
from Telemetry.colours import seat_colours
from Telemetry.subroutines import is_2d_list, average_Array_into_One_Percentage

def plot_line(y_array, x_array, title, yaxis_title, xaxis_title, names):
    fig = go.Figure()
    colours = list(seat_colours.values())

    if is_2d_list(y_array):
        iterations = 0
        for array in y_array:
            if names:
                name_value=f'{iterations + 1} | {names[iterations]}'
            else:
                name_value=f'{iterations + 1}'

            fig.add_trace(go.Scatter(
                x=x_array[iterations], 
                y=array, 
                name=name_value, 
                line=dict(color=colours[iterations])
            ))
            iterations += 1
    else:
        fig.add_trace(go.Scatter(
            x=x_array, 
            y=y_array, 
        ))

        fig.update_layout(
            xaxis=dict(
                gridcolor='grey',
                tickmode='array',
                tickvals=list(range(0, len(x_array))), 
                ticktext=x_array    
            )           
        )

    if title == 'Gate Force %':
        fig.add_trace(go.Scatter(
            x=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
            y=[20, 60, 85, 95, 100, 100, 95, 80, 55, 25, 0],
            mode="lines",
            name="Gold Target",
            line=dict(color="gold", width=3)
        ))

    fig.update_layout(
        title=title,
        yaxis_title=yaxis_title,
        xaxis_title = xaxis_title,
        template='plotly_white',
        xaxis=dict(
            gridcolor='grey',  # Dark navy grid           
        ),
        font=dict(
            color='grey'  # Default font color for text elements like legend
        ),
        paper_bgcolor="rgba(0,0,0,0)",   # outer area
        plot_bgcolor='rgba(0,0,0,0)'  # Transparent paper background
    )

    return pio.to_html(fig, full_html=False, include_plotlyjs='cdn', config={
        "responsive": True,
        "displayModeBar": False
    })