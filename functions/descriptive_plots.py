from functions.map_style import calculate_degree_centrality
import plotly.graph_objects as go
import numpy as np
import plotly as plt

# Create current centrality bar plot
def current_centrality_plot(track_data, comparison_data, selected_map, marks, translation):
    # Extract elements of currently visible map by checking timeline slider & fetching from comparison_data
    if comparison_data is not None:
        label = marks.get(str(selected_map))  # Fetch label based on the slider's value

        if label in comparison_data:  # Check if the label exists in comparison_data keys
            selected_date = label

            if selected_date is not None:
                elements = comparison_data[selected_date]['elements']

                # Calculate in- and out-degree centrality for all elements & store in degrees dictionary
                degrees = {element['data']['id']: {'out': 0, 'in': 0} for element in elements 
                           if 'source' not in element['data'] and 'target' not in element['data']}

                elements, degrees = calculate_degree_centrality(elements, degrees)

                # Prepare data for the plot
                node_ids = list(degrees.keys())
                in_degrees = [degrees[node]['in'] for node in node_ids]
                out_degrees = [degrees[node]['out'] for node in node_ids]

                fig = go.Figure(data=[
                go.Bar(
                    name=translation['plot_01_in'], 
                    x=node_ids, 
                    y=in_degrees, 
                    marker_color='rgba(156, 211, 225, 0.5)'  # Color with low opacity
                ),
                go.Bar(
                    name=translation['plot_01_out'], 
                    x=node_ids, 
                    y=out_degrees, 
                    marker_color='#9CD3E1'  # Solid color
                )
                ])

                # Update layout
                fig.update_layout(
                    barmode='group',
                    margin={'l': 20, 'r': 20, 't': 100, 'b': 5},
                    title={
                        'text': translation['plot_01_title'],
                        'y': 0.92,  # Adjust the vertical position of the title
                        'x': 0.5,
                        'xanchor': 'center',
                        'yanchor': 'top'
                    },
                    xaxis=dict(
                        tickangle=-45  # Rotate tick labels for better fit
                    ),
                    yaxis_title=translation['plot_01_y'],
                    template='plotly_white',
                    yaxis=dict(
                    tickmode='linear',
                    tick0=0,
                    dtick=1,  # Set the tick interval to 1 to show only whole numbers
                    tickformat='d'  # Ensure that the tick labels are displayed as integers
                ),
                legend=dict(
                orientation='h',  # Set the legend to horizontal
                yanchor='bottom',  # Anchor to the bottom of the legend box
                y=1,  # Position it slightly above the plot
                xanchor='center',  # Center the legend horizontally
                x=0.5,  # Set it in the middle of the plot
                ),
                font=dict(
                    family="Outfit",  # Set font family
                    size=14,          # Adjust font size
                    color="#333333"    # Set font color
                ),
                modebar_remove=['zoom', 'pan', 'select2d', 'lasso2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d'],
                modebar_add=['toImage'],  # 'toImage' adds the "save as PNG" button
                modebar=dict(
                    orientation='v',  # Vertical orientation for the modebar
                    bgcolor='rgba(0,0,0,0)',  # Transparent background
                    activecolor='#516395'  # Active button color
                )
                )

                # Return the figure
                return fig

    return None

# Create overall centrality line plot
def calculate_degree_ratios(elements):
    degrees = {element['data']['id']: {'out': 0, 'in': 0} for element in elements 
               if 'source' not in element['data'] and 'target' not in element['data']}
    elements, degrees = calculate_degree_centrality(elements, degrees)
    degree_ratios = {node: degrees[node]['out'] / degrees[node]['in'] if degrees[node]['in'] != 0 else degrees[node]['out'] for node in degrees}
    return degree_ratios

# Prepare data for severity overall plot
def prepare_graph_data(comparison_data):
    x = []
    y = []

    for network, data in comparison_data.items():
        severity = data.get('severity', {})
        elements = data.get('elements', [])

        # Extract valid factor names from the elements
        valid_factors = set([element['data']['label'] for element in elements if 'data' in element and 'label' in element['data']])

        # Filter the severity data to only include factors that are still in the elements
        filtered_severity = {factor: score for factor, score in severity.items() if factor in valid_factors}

        # Append the filtered severity data and the network name to x and y
        x.append(network)
        y.append(filtered_severity)

    return x, y