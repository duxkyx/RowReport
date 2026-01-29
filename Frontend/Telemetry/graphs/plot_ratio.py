import plotly.graph_objects as go
import plotly.io as pio
from telemetry.modules.checks import is_2d_list
from telemetry.graphs.colours import bar_colours

def create_ratio_plot(values, names=None):
    # Sample data
    categories = ['Recovery 1', '25% Recovery', 'Recovery 2', '50% Recovery', 'Recovery 3', '75% Recovery', 'Recovery 4',
                  'Hang 1', 'Min Angle', 'Hang 2', 'Catch Slip', 'Drive 1', 'Up-to 70% Peak Force', 'Drive 2', 'Peak Force', 'Drive 3', 'From 70% Peak Force', 'Drive 4',
                  'Finish Slip', 'Pause 1', 'Max Angle', 'Pause 2', 'Recovery 5']

    fig = go.Figure()

    if is_2d_list(values):
        # Each row represents a bar; each value segment is a stacked section
        for idx, row in enumerate(values):
            if names:
                name_value=f'{names[idx]} | {idx + 1} Seat'
            else:
                name_value=f'{idx + 1} | Seat'
            start = 0
            for i, val in enumerate(row):
                fig.add_trace(go.Bar(
                    x=[val],
                    y=[name_value],
                    orientation='h',
                    name=categories[i] if i < len(categories) else f'Segment {i+1}',
                    marker=dict(color=bar_colours[i]),
                    showlegend=(idx == 0)  # show legend only once
                ))
                start += val
    else:
        # Single row only
        for i, val in enumerate(values):
            fig.add_trace(go.Bar(
                x=[val],
                y=["Overall"],
                orientation='h',
                name=categories[i] if i < len(categories) else f'Segment {i+1}',
            ))

    fig.update_layout(
        barmode='stack',
        title='Ratios of Stroke Phases',
        xaxis_title='Time (ms)',
        yaxis_title='Seats',
        height=500,
        bargap=0,
        bargroupgap=0,
        margin=dict(l=100, r=50, t=50, b=50),
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