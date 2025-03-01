# Normalize        
def normalize(value, max_degree, min_degree):
    value = float(value)
    if max_degree - min_degree == 0:
        return 0.5  
    return (value - min_degree) / (max_degree - min_degree)

# Color gradient
# def get_color(value):
#     b = 255
#     r = int(173 * (1 - value))
#     g = int(216 * (1 - value))
#     return r, g, b

def get_color(value):
    """ Generates a lightness-based blue gradient from dark (#0A44F2) to light (#AEC2FF). """
    min_color = (174, 194, 255)  # Lightest blue (like low opacity)
    max_color = (10, 68, 242)    # Deep blue (full opacity effect)

    # Interpolate between min_color and max_color based on value (0 to 1)
    r = int(min_color[0] + (max_color[0] - min_color[0]) * value)
    g = int(min_color[1] + (max_color[1] - min_color[1]) * value)
    b = int(min_color[2] + (max_color[2] - min_color[2]) * value)

    return f'rgb({r}, {g}, {b})'  # ✅ Cytoscape-compatible


# Calculate degree centrality
def calculate_degree_centrality(elements, degrees):
    for element in elements:
        if 'source' in element['data']:
            source = element['data']['source']
            degrees[source]['out'] = degrees[source].get('out', 0) + 1
        if 'target' in element['data']:
            target = element['data']['target']
            degrees[target]['in'] = degrees[target].get('in', 0) + 1
    return elements, degrees

# Apply uniform color
def apply_uniform_color_styles(stylesheet):
    # Define the uniform color style for nodes
    uniform_color_style = {
        'selector': 'node',
        'style': {
            'background-color': '#0A44F2',
            'font-family': 'Outfit, sans-serif',
            'label': 'data(label)'  # Ensure labels are maintained
        }
    }
    # Remove any existing node color styles
    stylesheet = [style for style in stylesheet if 'background-color' not in style.get('style', {})]
    # Append the uniform color style
    stylesheet.append(uniform_color_style)
    return stylesheet

# Apply severity color
def apply_severity_color_styles(type, stylesheet, severity_scores, default_style):
    # Check if severity_scores is not empty and valid
    if severity_scores and all(isinstance(score, (int, float)) for score in severity_scores.values()):
        if type == "Severity":
            max_severity = max(severity_scores.values())
            min_severity = min(severity_scores.values())
        elif type == "Severity (abs)":
            max_severity = 10
            min_severity = 1

        # Check if max_severity and min_severity are the same (avoid normalization)
        if max_severity == min_severity:
            # Apply the same color for all nodes (no normalization)
            for node_id, severity in severity_scores.items():
                #r, g, b = get_color(1.0)  # Use a default value like 1.0 or any fixed color
                background_color = get_color(1.0)  # ✅ Correct: store the RGBA string directly

                severity_style = {
                    'selector': f'node[id="{node_id}"]',
                    'style': {
                        #'background-color': f'rgb({r},{g},{b})'
                        'background-color': background_color,
                        'font-family': 'Outfit, sans-serif'
                    }
                }
                # Append the style for this node
                stylesheet.append(severity_style)
        else:
            # Normalize and apply color based on severity
            for node_id, severity in severity_scores.items():
                normalized_severity = (severity - min_severity) / (max_severity - min_severity)
                #r, g, b = get_color(normalized_severity)  # Assuming get_color is defined
                background_color = get_color(normalized_severity)

                severity_style = {
                    'selector': f'node[id="{node_id}"]',
                    'style': {
                        #'background-color': f'rgb({r},{g},{b})'
                        'background-color': background_color,
                        'font-family': 'Outfit, sans-serif' 
                    }
                }
                # Append the style for this node
                stylesheet.append(severity_style)

    elif severity_scores == {}:
        stylesheet = default_style

    return stylesheet

# Apply degree centrality color
def apply_centrality_color_styles(type, stylesheet, elements):
    degrees = {element['data']['id']: {'out': 0, 'in': 0} for element in elements 
               if 'id' in element['data']}
    
    # Calculate in-degree and out-degree
    elements, degrees = calculate_degree_centrality(elements, degrees)

    # Compute centrality based on the selected type
    computed_degrees = {}
    for id, degree_counts in degrees.items():
        if type == "Out-degree":
            computed_degrees[id] = degree_counts['out']
        elif type == "In-degree":
            computed_degrees[id] = degree_counts['in']
        elif type == "Out-/In-degree ratio":
            if degree_counts['in'] != 0:
                computed_degrees[id] = degree_counts['out'] / degree_counts['in']
            else:
                computed_degrees[id] = 0  # or some other default value you deem appropriate
    if computed_degrees:
        min_degree = min(computed_degrees.values())
        max_degree = max(computed_degrees.values())
    else:
        min_degree = 0
        max_degree = 1

    for node_id, degree in computed_degrees.items():
        if max_degree != min_degree:
            # Normalized degree value when max and min degrees are different
            normalized_degree = (degree - min_degree) / (max_degree - min_degree)
        else:
            normalized_degree = 0.5 

        #r, g, b = get_color(normalized_degree) 
        background_color = get_color(normalized_degree)

        degree_style = {
            'selector': f'node[id="{node_id}"]',
            'style': {
                #'background-color': f'rgb({r},{g},{b})'
                'background-color': background_color,
                'font-family': 'Outfit, sans-serif'
            }
        }
        stylesheet.append(degree_style)

    return stylesheet

# Set color scheme
def color_scheme(chosen_scheme, graph_data, severity_scores):
    elements = graph_data['elements']
    stylesheet = graph_data['stylesheet']
    default_style = [{'selector': 'node','style': {'background-color': '#0A44F2', 'label': 'data(label)', 'font-family': 'Outfit, sans-serif'}},
                     {'selector': 'edge','style': {'curve-style': 'bezier', 'target-arrow-shape': 'triangle'}}]
    
    if chosen_scheme == "Uniform":
        graph_data['stylesheet'] = apply_uniform_color_styles(graph_data['stylesheet'])
    elif chosen_scheme in ["Severity", "Severity (abs)"]:
        graph_data['stylesheet'] = apply_severity_color_styles(chosen_scheme, graph_data['stylesheet'], severity_scores, default_style)
    elif chosen_scheme in ["Out-degree", "In-degree", "Out-/In-degree ratio"]:
        graph_data['stylesheet'] = apply_centrality_color_styles(chosen_scheme, graph_data['stylesheet'], elements)
    
    return graph_data

# Include edge properties 
def update_stylesheet(graph_data, edge_id, edge_type, strength):
    stylesheet = graph_data.get('stylesheet', [])

    # Define color mapping
    color_map = {
        'amplifier': '#C54B47',  # Red
        'reliever': '#004AAD',   # Blue
        'default': '#0A44F2'     # Default color
    }

    # Determine color based on edge type
    color = color_map.get(edge_type, color_map['default'])

    # Update edge style
    updated_edge_style = {
        'selector': f'edge[id="{edge_id}"]',
        'style': {
            'line-color': color,
            'target-arrow-color': color,
            'source-arrow-color': color,
            'opacity': strength / 5
        }
    }

    # Remove old style and add new style
    updated_stylesheet = [rule for rule in stylesheet if rule['selector'] != f'edge[id="{edge_id}"]']
    updated_stylesheet.append(updated_edge_style)

    # Update graph_data
    graph_data['stylesheet'] = updated_stylesheet

    return graph_data

# Normalize size
def normalize_size(value, max_value, min_value, min_size, max_size):
    if max_value == min_value:
        # If max and min values are equal, return the average size to avoid division by zero
        return (max_size + min_size) / 2

    # Normalize the value to a range between min_size and max_size
    normalized = (value - min_value) / (max_value - min_value)
    return normalized * (max_size - min_size) + min_size

# Apply uniform node sizing 
def apply_uniform_size_styles(stylesheet):
    # Define the uniform size style
    uniform_size_style = {
        'selector': 'node',
        'style': {'width': 25, 'height': 25, 'font-family': 'Outfit, sans-serif'}  # Example sizes
    }
    # Apply this style to the stylesheet
    stylesheet = [style for style in stylesheet if 'width' not in style.get('style', {})]
    stylesheet.append(uniform_size_style)

    return stylesheet

# Apply severity node sizing
def apply_severity_size_styles(type, stylesheet, severity_scores, default_style):
    # Check if severity_scores is not empty and valid
    max_size = 50
    min_size = 10

    #print(severity_scores.items())
    if severity_scores and all(isinstance(score, (int, float)) for score in severity_scores.values()):
        if type == "Severity":
            max_severity = max(severity_scores.values())
            min_severity = min(severity_scores.values())
        elif type == "Severity (abs)":
            max_severity = 10
            min_severity = 1

        # Normalize and apply color based on severity
        for node_id, severity in severity_scores.items():
            size = normalize_size(severity, max_severity, min_severity, min_size, max_size)

            severity_style = {
                'selector': f'node[id="{node_id}"]',
                'style': {'width': size,'height': size, 'font-family': 'Outfit, sans-serif'}
                }
            
            # Append the style for this node
            stylesheet.append(severity_style)

    elif severity_scores == {}:
        stylesheet = default_style
        #return dash.no_update

    return stylesheet

# Apply degree centraliy node sizing
def apply_centrality_size_styles(type, stylesheet, elements):
    max_size = 50
    min_size = 10

    degrees = {element['data']['id']: {'out': 0, 'in': 0} for element in elements 
               if 'id' in element['data']}
    
    # Calculate in-degree and out-degree
    elements, degrees = calculate_degree_centrality(elements, degrees)

    # Compute centrality based on the selected type
    computed_degrees = {}
    for id, degree_counts in degrees.items():
        if type == "Out-degree":
            computed_degrees[id] = degree_counts['out']
        elif type == "In-degree":
            computed_degrees[id] = degree_counts['in']
        elif type == "Out-/In-degree ratio":
            if degree_counts['in'] != 0:
                computed_degrees[id] = degree_counts['out'] / degree_counts['in']
            else:
                computed_degrees[id] = 0  # or some other default value you deem appropriate

    if computed_degrees:
        min_degree = min(computed_degrees.values())
        max_degree = max(computed_degrees.values())
    else:
        min_degree = 0
        max_degree = 1

    for node_id, degree in computed_degrees.items():
        size = normalize_size(degree, max_degree, min_degree, min_size, max_size)

        degree_style = {
            'selector': f'node[id="{node_id}"]',
            'style': {'width': size, 'height': size, 'font-family': 'Outfit, sans-serif'}
        }

        # Append the style for this node
        stylesheet.append(degree_style)

    return stylesheet

# Set node sizing scheme 
def node_sizing(chosen_scheme, graph_data, severity_scores):
    print(severity_scores)
    elements = graph_data['elements']
    stylesheet = graph_data['stylesheet']
    default_style = [{'selector': 'node','style': {'background-color': '#0A44F2', 'label': 'data(label)', 'font-family': 'Outfit, sans-serif'}},
                     {'selector': 'edge','style': {'curve-style': 'bezier', 'target-arrow-shape': 'triangle'}}]
    
    if chosen_scheme == "Uniform":
        graph_data['stylesheet'] = apply_uniform_size_styles(graph_data['stylesheet'])
    elif chosen_scheme in ["Severity", "Severity (abs)"]:
        graph_data['stylesheet'] = apply_severity_size_styles(chosen_scheme, graph_data['stylesheet'], severity_scores, default_style)
    elif chosen_scheme in ["Out-degree", "In-degree", "Out-/In-degree ratio"]:
        graph_data['stylesheet'] = apply_centrality_size_styles(chosen_scheme, graph_data['stylesheet'], elements)
    
    return graph_data

# Color most influential fator in graph 
def color_target(graph_data):
    influential_factor = graph_data['dropdowns']['target']['value']
    stylesheet = graph_data['stylesheet']

    if influential_factor:
        stylesheet.append({'selector': f'node[id = "{influential_factor[0]}"]',
                           'style': {'border-color': '#BF00FF','border-width': '2px', 'font-family': 'Outfit, sans-serif'}})
        
    graph_data['stylesheet'] = stylesheet
    return graph_data

# Reset target color
def reset_target(graph_data):
    stylesheet = graph_data['stylesheet']
    new_stylesheet = [style for style in stylesheet 
                      if not (style.get('style', {}).get('border-color') == '#BF00FF')]
    graph_data['stylesheet'] = new_stylesheet
    return graph_data

# Color graph (out-degree centrality, target node)
def graph_color(session_data, severity_scores):

    session_data = reset_target(session_data)
    session_data = color_target(session_data)

    session_data = node_sizing(chosen_scheme="Severity", graph_data=session_data, severity_scores=severity_scores)

    return session_data

# Updates edge styles based on strength
def update_edge_opacity(edge_id, strength, stylesheet):
    opacity = strength / 5  # Adjust opacity based on strength
    tapped_edge_style = {
        'selector': f'edge[id="{edge_id}"]',
        'style': {'opacity': opacity}
    }
    # Create a new stylesheet with updated style for the edge
    new_stylesheet = [rule for rule in stylesheet if rule['selector'] != f'edge[id="{edge_id}"]']
    new_stylesheet.append(tapped_edge_style)
    return new_stylesheet

# Helper function to apply uniform color and severity size styles
def apply_uniform_style(elements, severity_scores, uniform_color, stylesheet):
    # First, apply the severity-based sizing
    stylesheet = apply_severity_size_styles("Severity", stylesheet, severity_scores, stylesheet)

    # Then, override the color with the uniform color for all nodes
    for element in elements:
        if 'data' in element and 'id' in element['data']:
            node_id = element['data']['id']
            uniform_style = {
                'selector': f'node[id="{node_id}"]',
                'style': {
                    'background-color': uniform_color,
                    'font-family': 'Outfit, sans-serif'
                }
            }
            stylesheet.append(uniform_style)

    return stylesheet
