import plotly.graph_objects as go
import plotly.io as pio
from telemetry.graphs.colours import seat_colours, seat_effective_colours, sample_colours
from telemetry.modules.checks import is_2d_list

def plot_line(x_array, y_array, title, x_label, y_label, names, pdf, optional_values=None, catchnormalized=False, finishnormalized=False, athlete_data=False, graph_Order=0, highlight_Effective=False):
    fig = go.Figure()
    colours = list(seat_colours.values())
    effective_colours = list(seat_effective_colours.values())
    samples_colour = list(sample_colours.values())

    if is_2d_list(y_array):
        # Iterate through the array holding the values for each athlete. (8 arrays for 8 athletes)
        for iterations in range(len(y_array)):
            try:
                # Add the names if they exist.
                if names:
                    name_value=f'{iterations + 1} | {names[iterations]}'

                # Define current athlete values
                x_vals = x_array[iterations]
                y_vals = y_array[iterations]

                # Special case for seat position to change line colour based on gateforcex
                if highlight_Effective:
                    gateforce_vals = optional_values[iterations]

                    current_x = []
                    current_y = []

                    found_Effective_Start = False
                    highlight = gateforce_vals[0] >= 30

                    for iteration_2 in range(len(y_vals)):
                        gateforce = gateforce_vals[iteration_2]
                        if not found_Effective_Start:
                            new_highlight = gateforce >= 30
                        else:
                            new_highlight = gateforce >= 15

                        if new_highlight != highlight and current_x:

                            # Effective start: >= 30kg, Effective end >= 15kg. Therefore once started, lower threshold to avoid missing values.
                            if not found_Effective_Start:
                                found_Effective_Start = True

                            fig.add_trace(go.Scatter(
                                x=current_x, 
                                y=current_y, 
                                mode="lines",
                                name=name_value,
                                legendgroup=name_value,
                                showlegend=False, 
                                line=dict(
                                    color=effective_colours[iterations] if highlight else colours[iterations]
                                )
                            ))

                            current_x = []
                            current_y = []
                        
                        current_x.append(x_vals[iteration_2])
                        current_y.append(y_vals[iteration_2])
                        highlight = new_highlight
                        
                    fig.add_trace(go.Scatter(
                        x=current_x, 
                        y=current_y, 
                        name=name_value, 
                        legendgroup=name_value,
                        showlegend=True,
                        mode="lines",
                        line=dict(
                            color=colours[iterations] if athlete_data else samples_colour[iterations]
                        )
                    ))
                else:
                    fig.add_trace(go.Scatter(
                        x=x_vals, 
                        y=y_vals, 
                        name=name_value, 
                        line=dict(color=colours[iterations] if athlete_data else samples_colour[iterations])
                    ))
                iterations += 1
            except:
                iterations += 1
                continue
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

    if catchnormalized:
        fig.add_vline(
            x=catchnormalized[graph_Order] if type(catchnormalized) == list else catchnormalized,
            line_width=2,
            line_dash="dash",
            line_color="black",
            annotation_text="Catch",
            annotation_position="top"
        )
        
        fig.add_vline(
            x=finishnormalized[graph_Order] if type(finishnormalized) == list else finishnormalized,
            line_width=2,
            line_dash="dash",
            line_color="black",
            annotation_text="Finish",
            annotation_position="top"
        )

    fig.update_layout(
        title=None if pdf else title,
        showlegend=False if pdf else True,
        xaxis_title=x_label,
        yaxis_title=y_label,
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
                "scrollZoom": False,
                "displaylogo": False,
                "toImageButtonOptions": {
                    "format": "png",
                    "filename": "rowreport_export"
                }
            }
        )