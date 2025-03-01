import dash, json, base64
import copy

from app import app
from datetime import datetime
from dash import dcc, Input, Output, State, ALL, MATCH, callback_context
from constants import translations
from functions.map_build import delete_edge
from functions.map_style import (node_sizing, calculate_degree_centrality, color_scheme)
from functions.data_format import (format_export_data, send_to_github)
from functions.page_content import (create_likert_scale)
from datetime import datetime

# Set edit graph to PsySys graph when user clicks on "redirect" button at the end of PsySys session
def redirect_edit(n_clicks, session_data, severity_scores):
    if n_clicks:
        severity_scores_edit = severity_scores.copy()
        # Ensure you're working with a copy of the session data, not the original data
        session_data_copy = {
            'elements': session_data['elements'].copy(), 
            'stylesheet': session_data['stylesheet'].copy(),
            'severity': session_data.get('severity', {}).copy()  # Clone severity to prevent direct modification
        }
        return session_data_copy, severity_scores_edit
    # Return no update if the button wasn't clicked
    return dash.no_update

# Set edit-graph to session-data if "Load from session" is pressed
def load_session_graph(n_clicks, session_data, severity_scores):
    if n_clicks:
        severity_scores_edit = severity_scores.copy()
        # Ensure you're working with a copy of the session data, not the original data
        session_data_copy = {
            'elements': session_data['elements'].copy(), 
            'stylesheet': session_data['stylesheet'].copy(),
            'severity': session_data.get('severity', {}).copy()  # Clone severity to prevent direct modification
        }
        return session_data_copy, severity_scores_edit
    # Return no update if the button wasn't clicked
    return dash.no_update

# Generate download file  
def generate_download(n_clicks, data, severity_scores, annotations, edge_data, current_style):
    if n_clicks:
        elements = data['elements']
        current_date = datetime.now().strftime("%y/%m/%d-%H:%M")
        # Calculate & include: degree centralities
        degrees = {element['data']['id']: {'out': 0, 'in': 0} for element in elements 
               if 'id' in element['data']}
    
        # Calculate in-degree and out-degree
        elements, degrees = calculate_degree_centrality(elements, degrees)

        # Compute centrality based on the selected type
        out_degrees = {}
        in_degrees = {}
        out_in_ratio = {}
        for id, degree_counts in degrees.items():
            out_degrees[id] = degree_counts['out']
            in_degrees[id] = degree_counts['in']

            if degree_counts['in'] != 0:
                out_in_ratio[id] = degree_counts['out'] / degree_counts['in']
            else:
                out_in_ratio[id] = 0 

        # Format data to be exported 
        # Filter out: elements, stylesheet, edges
        # Include: annotations, severity scores, edge_data, degree centralities
        exported_data = {
            'elements': data['elements'],
            'stylesheet': current_style,
            'edges': data.get('edges'),
            'severity-scores': severity_scores,
            'edge-data': edge_data,
            'out-degrees': out_degrees,
            'in-degrees': in_degrees,
            'out-in-ratio': out_in_ratio,
            'annotations': annotations,
            'date': current_date
        }

        # Append the date to the file name
        file_name = f"my_mental_health_map_{current_date}.json"

        # Convert the dictionary to a JSON string
        json_string = json.dumps(exported_data)
        return dcc.send_bytes(json_string.encode('utf-8'), file_name)
    return dash.no_update

# Upload existing map file
def upload_graph(contents, filename):
    if contents:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        data = json.loads(decoded.decode('utf-8'))
        return data
    return dash.no_update

# Open edit node modal upon clicking it
def open_node_edit_modal(tapNodeData, switch, severity_scores, annotations):
    #if editing_mode == 'mode-1':
    if 0 not in switch and tapNodeData:
        node_id = tapNodeData['id']
        node_name = tapNodeData.get('label', node_id)
        severity_score = severity_scores.get(node_name, 0)
        annotation = annotations.get(node_id, '') 

        return True, node_name, severity_score, annotation
    
    return False, '', 0, ''  # Closed modal with default values
        # return False, None, None, ''

# Reset tabnodedata on mode switch
def reset_tap_data(switch):
    return {}, {}

# Update the annotation for the node
def update_annotations(note_input, tapNodeData, annotations):
    if tapNodeData:
        node_id = tapNodeData['id']
        annotations[node_id] = note_input 
    return annotations

# Save node changes and apply severity changes to schemes, if applicable
def save_node_changes_and_apply_schemes(n_clicks, selected_color_scheme, selected_scheme, new_name, new_severity, 
                                        elements, severity_scores, edit_map_data, tapNodeData):
    # Initialize severity_scores_copy with a deep copy of severity_scores
    severity_scores_copy = copy.deepcopy(severity_scores)

    if n_clicks and tapNodeData:
        old_node_id = tapNodeData['id']

        # Update node name in elements
        for element in elements:
            if element.get('data', {}).get('id') == old_node_id:
                element['data']['label'] = new_name

        # Update severity score in the copied version
        severity_scores_copy[old_node_id] = new_severity
        severity_scores_copy[new_name] = new_severity

        # Update edit_map_data with the changed elements
        edit_map_data['elements'] = elements

    # Check and apply color scheme
    if selected_color_scheme is None: 
        edit_map_data = color_scheme('Uniform', edit_map_data, severity_scores)

    if selected_color_scheme is not None and edit_map_data is not None and severity_scores_copy is not None:
        edit_map_data = color_scheme(selected_color_scheme, 
                                     edit_map_data, 
                                     severity_scores_copy)

    # Check and apply node sizing scheme
    if selected_scheme is None: 
        edit_map_data = node_sizing('Severity', edit_map_data, severity_scores)

    if selected_scheme is not None and edit_map_data is not None and severity_scores_copy is not None:
        edit_map_data = node_sizing(chosen_scheme=selected_scheme, 
                                    graph_data=edit_map_data, 
                                    severity_scores=severity_scores_copy)

    # Ensure stylesheet is updated based on the above changes
    stylesheet = edit_map_data.get('stylesheet', [])

    # Return the deep-copied severity scores to prevent accidental modification of the original scores
    return elements, severity_scores_copy, edit_map_data, stylesheet, selected_scheme, selected_color_scheme


# Open edge edit modal
def open_edge_edit_modal(tapEdgeData, switch, edge_data, language):

    translation = translations.get(language, translations['en'])

    if edge_data is None:
        edge_data = {}

    if 0 not in switch and tapEdgeData:
        edge_id = tapEdgeData['id']
        explanation = translation['text_edge_01'] + " " + tapEdgeData['source'] + " " + translation['text_edge_02'] + " " + tapEdgeData['target']
        strength = edge_data.get(edge_id, {}).get('strength', 5)
        annotation = edge_data.get(edge_id, {}).get('annotation', '')
        return True, explanation, strength, annotation

    return False, '', 5, ''

def open_modal_on_edge_tap(tapEdgeData, switch, is_open, edge_data):
    # Check if the edge is tapped and the switch is not in state 0
    if tapEdgeData and 0 not in switch:
        edge_id = tapEdgeData['id']

        # Retrieve the stored type for this edge, defaulting to 'Default' if not set
        edge_type = edge_data.get(edge_id, {}).get('type', 'Default')
        
        return True, edge_type  # Open the modal and set the dropdown to the current or default edge type

    return is_open, dash.no_update

# Save edge changes & close modal 
def save_edge_changes_and_close_modal(save_clicks, tapEdgeData, strength, annotation, edge_data, edit_map_data, current_stylesheet, edge_type):
    ctx = callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    # Initialize edge_data and edit_map_data
    if edge_data is None:
        edge_data = {}
    if edit_map_data is None:
        edit_map_data = {}

    stylesheet = current_stylesheet or []

    # Handle Save Button Click
    if triggered_id == 'edge-save-btn' and save_clicks and tapEdgeData:
        edge_id = tapEdgeData['id']

        # Update the edge data with strength, annotation, and type
        edge_data[edge_id] = {
            'strength': strength,
            'annotation': annotation,
            'type': edge_type  # Save the selected edge type
        }

        # Update the stylesheet for the tapped edge
        opacity = strength / 5  # Adjust opacity based on strength
        if edge_type == 'amplifier':
            color = '#C54B47'
        elif edge_type == 'reliever':
            color = '#004AAD'
        else: 
            color = '#999999'  # Default Cytoscape.js edge color

        tapped_edge_style = {
            'selector': f'edge[id="{edge_id}"]',
            'style': {
                'opacity': opacity,
                'line-color': color,
                'target-arrow-color': color,
                'source-arrow-color': color
            }
        }

        # Create a new stylesheet with updated style for the tapped edge
        new_stylesheet = [rule for rule in stylesheet if rule['selector'] != f'edge[id="{edge_id}"]']
        new_stylesheet.append(tapped_edge_style)

        # Save updated data in edit-map-data
        edit_map_data['stylesheet'] = new_stylesheet
        edit_map_data['edges'] = edge_data

        # Close the modal after saving
        return edge_data, new_stylesheet, edit_map_data, False

    # Default: keep the current modal state
    return edge_data, stylesheet, edit_map_data, dash.no_update

# Edit map - add node & apply changes to schemes, if applicable 
def map_add_node_01(n_clicks, node_name, elements, edit_map_data, severity_scores, history, 
                    selected_color_scheme, selected_scheme):
    if n_clicks and node_name:
        if not any(node['data']['id'] == node_name for node in elements):

            # Save current state to history
            #history.append(edit_map_data)
            history.append({
            'elements': elements.copy(),
            'edit_map_data': edit_map_data.copy(),
            'severity_scores': severity_scores.copy()
            })

            new_node = {'data': {'id': node_name, 'label': node_name}}
            elements.append(new_node)
            severity_scores[node_name] = 5  # Add new node with default severity score

    node_names = [node['data']['id'] for node in elements if 'id' in node['data'] and len(node['data']['id']) < 30]
    edit_map_data['add-nodes'] = node_names
    edit_map_data['elements'] = elements

    cytoscape_elements = edit_map_data.get('elements', [])
    options_1 = [{'label': element['data'].get('label', element['data'].get('id')), 'value': element['data'].get('id')} for element in cytoscape_elements if 'data' in element and 'label' in element['data'] and 'id' in element['data']]
    
    # Check and apply color scheme
    if selected_color_scheme is None: 
        edit_map_data = color_scheme('Uniform', edit_map_data, severity_scores)
    
    if selected_color_scheme is not None and edit_map_data is not None and severity_scores is not None:
        edit_map_data = color_scheme(selected_color_scheme, 
                                     edit_map_data, 
                                     severity_scores)

    # Check and apply node sizing scheme
    if selected_scheme is None: 
        edit_map_data = node_sizing('Severity', edit_map_data, severity_scores)

    if selected_scheme is not None and edit_map_data is not None and severity_scores is not None:
        edit_map_data = node_sizing(chosen_scheme=selected_scheme, 
                                    graph_data=edit_map_data, 
                                    severity_scores=severity_scores)

    # Ensure stylesheet is updated based on the above changes
    stylesheet = edit_map_data.get('stylesheet', [])

    return elements, options_1, edit_map_data, severity_scores, history, stylesheet

# Remove existing node from graph & apply changes to schemes, if applicable 
def delete_node_01(n_clicks, node_id, elements, edit_map_data, severity_scores, history, 
                   selected_color_scheme, selected_scheme):
    if n_clicks and node_id:

        history.append({
            'elements': elements.copy(),
            'edit_map_data': edit_map_data.copy(),
            'severity_scores': severity_scores.copy()
        })

        # Delete node from elements
        elements = [element for element in elements if element['data'].get('id') != node_id]
        # Delete any existing edges from elements which contain this node
        elements = [element for element in elements if not (('source' in element['data'] and element['data']['source'] == node_id) or ('target' in element['data'] and element['data']['target'] == node_id))]

        if node_id in severity_scores:
            del severity_scores[node_id]  # Remove node from severity scores

    node_names = [node['data']['id'] for node in elements if 'id' in node['data'] and len(node['data']['id']) < 30]
    edit_map_data['add-nodes'] = node_names
    edit_map_data['elements'] = elements

    cytoscape_elements = edit_map_data.get('elements', [])
    options_1 = [{'label': element['data'].get('label', element['data'].get('id')), 'value': element['data'].get('id')} for element in cytoscape_elements if 'data' in element and 'label' in element['data'] and 'id' in element['data']]

    # Check and apply color scheme
    if selected_color_scheme is None: 
        edit_map_data = color_scheme('Uniform', edit_map_data, severity_scores)
    
    if selected_color_scheme is not None and edit_map_data is not None and severity_scores is not None:
        edit_map_data = color_scheme(selected_color_scheme, 
                                     edit_map_data, 
                                     severity_scores)

    # Check and apply node sizing scheme
    if selected_scheme is None: 
        edit_map_data = node_sizing('Severity', edit_map_data, severity_scores)

    if selected_scheme is not None and edit_map_data is not None and severity_scores is not None:
        edit_map_data = node_sizing(chosen_scheme=selected_scheme, 
                                    graph_data=edit_map_data, 
                                    severity_scores=severity_scores)

    # Ensure stylesheet is updated based on the above changes
    stylesheet = edit_map_data.get('stylesheet', [])

    return elements, options_1, edit_map_data, severity_scores, history, stylesheet

# Limit dropdown for edit-edge to 2
def limit_dropdown_edit_edge(edit_edge):
    if edit_edge and len(edit_edge) > 2:
        return edit_edge[:2]
    return edit_edge

# Add additional edge to graph & apply changes to schemes, if applicable 
def add_edge_output_01(n_clicks, new_edge, elements, edit_map_data, severity_scores, history, edge_data, selected_color_scheme, selected_scheme):
    if n_clicks and new_edge and len(new_edge) == 2:
        # Save current state to history
        history.append({
            'elements': elements.copy(),
            'edit_map_data': edit_map_data.copy(),
            'severity_scores': severity_scores.copy(),
            'edge_data': edge_data.copy()  # Ensure to also copy edge_data to history
        })

        source, target = new_edge

        # Initialize edge_data if it is None
        if edge_data is None:
            edge_data = {}

        # Create a unique edge ID and add the new edge
        edge_id = f"edge_{source}_{target}"  # Ensure a unique edge ID
        if edge_id not in edge_data:
            # Initialize new edge data with default values
            edge_data[edge_id] = {
                'strength': 3,  # Default strength
                'annotation': '',  # Default annotation
                'type': 'default'  # Default type
            }

        # Assuming edit_map_data['edges'] is a list of edge dictionaries
        existing_edges = set(f"{e['data']['source']}->{e['data']['target']}" for e in elements if 'source' in e.get('data', {}))

        # Add the new edge to elements for visualization with a unique ID
        elements.append({
            'data': {
                'id': edge_id,
                'source': source,
                'target': target
            }
        })
        existing_edges.add(f"{source}->{target}")

        # Update edit_map_data with the new edges
        edit_map_data['edges'] = [{'data': {'id': f"edge_{src}_{tgt}_{i}", 'source': src, 'target': tgt}}
                                  for i, (src, tgt) in enumerate((edge.split('->') for edge in existing_edges))]
        edit_map_data['elements'] = elements

        # Explicitly update the stylesheet to ensure it includes the new edge
        new_stylesheet = edit_map_data.get('stylesheet', [])
        tapped_edge_style = {
            'selector': f'edge[id="{edge_id}"]',
            'style': {
                'opacity': 0.6,  # Default opacity
                'line-color': '#999999',  # Default color
                'target-arrow-color': '#999999',
                'source-arrow-color': '#999999'
            }
        }
        new_stylesheet.append(tapped_edge_style)
        edit_map_data['stylesheet'] = new_stylesheet

        # Check and apply color scheme
        if selected_color_scheme is None: 
            edit_map_data = color_scheme('Uniform', edit_map_data, severity_scores)

        if selected_color_scheme is not None and edit_map_data is not None and severity_scores is not None:
            edit_map_data = color_scheme(selected_color_scheme, 
                                         edit_map_data, 
                                         severity_scores)

        # Check and apply node sizing scheme
        if selected_scheme is None: 
            edit_map_data = node_sizing('Severity', edit_map_data, severity_scores)

        if selected_scheme is not None and edit_map_data is not None and severity_scores is not None:
            edit_map_data = node_sizing(chosen_scheme=selected_scheme, 
                                        graph_data=edit_map_data, 
                                        severity_scores=severity_scores)

        # Ensure stylesheet is updated based on the above changes
        stylesheet = edit_map_data.get('stylesheet', [])


        return elements, edit_map_data, history, edge_data, stylesheet

    return elements, edit_map_data, history, edge_data, edit_map_data['stylesheet']

# Delete existing edge from graph & apply changes to schemes, if applicable 
def delete_edge_output_01(n_clicks, edge, elements, edit_map_data, severity_scores, history, edge_data, selected_color_scheme, selected_scheme):
    if n_clicks and edge and len(edge) == 2:
        # Save current state to history
        history.append({
            'elements': elements.copy(),
            'edit_map_data': edit_map_data.copy(),
            'severity_scores': severity_scores.copy(),
            'edge_data': edge_data.copy()  # Save edge_data in history for undo functionality
        })

        source, target = edge

        # Identify the edge ID (assuming the format used earlier in add_edge_output)
        edge_id = f"edge_{source}_{target}"

        # Remove the edge from elements and existing edges set
        existing_edges = set([(e['data']['source'], e['data']['target']) 
                              for e in elements if 'source' in e.get('data', {})])
        delete_edge(source, target, elements, existing_edges)

        # Remove the edge from edge_data
        if edge_id in edge_data:
            del edge_data[edge_id]

        # Update edit_map_data
        edit_map_data['edges'] = list(existing_edges)
        edit_map_data['elements'] = elements

        # Check and apply color scheme
        if selected_color_scheme is None: 
            edit_map_data = color_scheme('Uniform', edit_map_data, severity_scores)

        if selected_color_scheme is not None and edit_map_data is not None and severity_scores is not None:
            edit_map_data = color_scheme(selected_color_scheme, edit_map_data, severity_scores)

        # Check and apply node sizing scheme
        if selected_scheme is None: 
            edit_map_data = node_sizing('Severity', edit_map_data, severity_scores)

        if selected_scheme is not None and edit_map_data is not None and severity_scores is not None:
            edit_map_data = node_sizing(chosen_scheme=selected_scheme, 
                                        graph_data=edit_map_data, 
                                        severity_scores=severity_scores)

        # Ensure stylesheet is updated based on the above changes
        stylesheet = edit_map_data.get('stylesheet', [])

    return elements, edit_map_data, history, edge_data, edit_map_data['stylesheet']

# Dynamically generate Likert scales
def update_likert_scales(selected_factors, severity_scores):
    if severity_scores is None:
        severity_scores = {}
    if selected_factors is None:
        return []
    return [create_likert_scale(factor, severity_scores.get(factor, 0)) for factor in selected_factors]


# Update severity scores
def update_severity_scores(severity_values, session_data, existing_severity_scores, edit_map_data):
    # Check if severity_values, session_data or existing_severity_scores is None
    if severity_values is None or session_data is None or existing_severity_scores is None:
        return dash.no_update

    # Initialize severity scores if not present
    if existing_severity_scores is None:
        existing_severity_scores = {}

    # Get the current list of factors
    current_factors = [
        element['data']['label'] 
        for element in edit_map_data['elements'] 
        if 'source' not in element['data'] and 'target' not in element['data']  # This means it's a node, not an edge
    ]

    # Ensure current_factors is not None
    if current_factors is None:
        return dash.no_update

    # Update the existing severity scores with new values
    for factor, value in zip(current_factors, severity_values):
        existing_severity_scores[factor] = value

    return existing_severity_scores

# Update sizing_scheme dropdown value
def update_custom_color_dropdown(value):
    return value

# Save edge type (reliver, amplifier)
def save_edge_type(n_clicks, edge_name, edge_type, edge_data):
    if n_clicks > 0 and edge_name and edge_type:
        # Initialize edge_data as a dictionary if it is None
        if edge_data is None:
            edge_data = {}

        # Update edge type data with the edge name as key
        edge_data[edge_name] = edge_type
        return edge_data

    # Return the existing edge_data if no new data is to be saved
    return edge_data

# Inspect node (highlight direct effects) upon clicking
def update_stylesheet_01(tapNodeData, switch, edit_map_data):
    default_stylesheet = edit_map_data['stylesheet']
    elements = edit_map_data['elements']

    # if editing_mode != 'mode-1':
    #     return default_stylesheet
    
    # Reset to default if in view mode
    if 0 not in switch:
        return default_stylesheet

    # If in inspect mode and a node is clicked
    if 0 in switch and tapNodeData:
        clicked_node_id = tapNodeData['id']
        # Find outgoing edges from the clicked node
        outgoing_edges = [e for e in elements if e.get('data', {}).get('source') == clicked_node_id]
        # Find target nodes of these edges
        target_node_ids = {e['data']['target'] for e in outgoing_edges}

        # Adjust the stylesheet for highlighting
        new_stylesheet = []
        for style in default_stylesheet:
            selector = style.get('selector')
            if 'node' in selector or 'edge' in selector:
                # Reduce opacity for all nodes and edges initially
                style['style']['opacity'] = '0.2'
                new_stylesheet.append(style)

        # Highlight the clicked node, its outgoing edges, and target nodes
        new_stylesheet.extend([
            {'selector': f'node[id = "{clicked_node_id}"]', 'style': {'opacity': '1'}},
            {'selector': ','.join([f'node[id = "{n_id}"]' for n_id in target_node_ids]), 'style': {'opacity': '1'}},
            {'selector': ','.join([f'edge[source = "{clicked_node_id}"][target = "{e["data"]["target"]}"]' 
                                   for e in outgoing_edges]), 'style': {'opacity': '1'}}
        ])

        return new_stylesheet
    # Return default if no node is clicked or if mode is not 'inspect'
    return default_stylesheet

# Open inspect info modal 
def inspect_info(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open

# Open color info modal 
def toggle_modal_color(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open

# Populate color info modal
def update_modal_content_color(selected_scheme, language):

    translation = translations.get(language, translations['en'])

    if selected_scheme == 'Uniform':
        return translation['modal_color_uniform']
    if selected_scheme == 'Severity':
        return translation['modal_color_severity']
    elif selected_scheme == 'Severity (abs)':
        return translation['modal_color_severity_abs']
    elif selected_scheme == 'Out-degree':
        return translation['modal_color_out']
    elif selected_scheme == 'In-degree':
        return translation['modal_color_in']
    elif selected_scheme == 'Out-/In-degree ratio':
        return translation['modal_color_out-in']
    return translation['modal_color_default']

# Open sizing info modal 
def toggle_modal_sizing(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open

# Populate sizing info modal 
def update_modal_content_sizing(selected_scheme, language):

    translation = translations.get(language, translations['en'])

    if selected_scheme == 'Uniform':
        return translation['modal_size_uniform']
    if selected_scheme == 'Severity':
        return translation['modal_size_severity']
    elif selected_scheme == 'Severity (abs)':
        return translation['modal_size_severity_abs']
    elif selected_scheme == 'Out-degree':
        return translation['modal_size_out']
    elif selected_scheme == 'In-degree':
        return translation['modal_size_in']
    elif selected_scheme == 'Out-/In-degree ratio':
        return translation['modal_size_out-in']
    return translation['modal_size_default']

# Download network as image
# def get_image(n_clicks):
#     # File type to output of 'svg, 'png', 'jpg', or 'jpeg' (alias of 'jpg')
#     ftype = 'jpg'

#     # 'store': Stores the image data in 'imageData' !only jpg/png are supported
#     # 'download'`: Downloads the image as a file with all data handling
#     # 'both'`: Stores image data and downloads image as file.
#     action = 'store'

#     file_name = 'my_image'  # Default file name

#     if n_clicks:
#         action = 'download'
#         #current_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#         current_date = datetime.now().strftime("%y/%m/%d-%H:%M")
#         file_name = f"my_mental_health_map_snapshot_{current_date}.{ftype}"

#     return {
#         'type': ftype,
#         'action': action,
#         'filename': file_name  # Set the filename for download
#     }

# def get_image(n_clicks, image_data):
#     if n_clicks:
#         print(f"Button clicked: n_clicks={n_clicks}")
#         print(image_data)
#         if image_data:
#             print("Image data received")
#             print(image_data)  # Print the data to see the format
            
#             ftype = 'jpg'
#             current_date = datetime.now().strftime("%y_%m_%d-%H%M")
#             file_name = f"my_mental_health_map_snapshot_{current_date}.{ftype}"

#             # If `image_data` includes a base64 prefix, split it
#             base64_content = image_data.split(",")[1] if "," in image_data else image_data

#             # Prepare download dictionary
#             download_dict = {
#                 "filename": file_name,
#                 "content": base64_content,
#                 "base64": True,
#                 "type": ftype
#             }
#             print(download_dict)  # Debug print to check download dictionary format
#             return download_dict

#     return dash.no_update  # If not clicked or no data received

def trigger_image_generation(n_clicks):
    if n_clicks:
        return {'type': 'jpg', 'action': 'store'}
    return dash.no_update

def get_image(image_data, n_clicks):
    if n_clicks and image_data:
        ftype = 'jpg'
        current_date = datetime.now().strftime("%y_%m_%d-%H%M")
        file_name = f"my_mental_health_map_snapshot_{current_date}.{ftype}"
        base64_content = image_data.split(",")[1] if "," in image_data else image_data
        download_dict = {
            "filename": file_name,
            "content": base64_content,
            "base64": True,
            "type": ftype
        }
        print("Download dictionary prepared:", download_dict)
        return download_dict
    return dash.no_update

# Donation 
def donation_modal(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open

# Donation button functionality
def donate_button_clicked(n_clicks, data, current_style, severity_scores, edge_data, annotations, is_open):
    if n_clicks:
        graph_data = format_export_data(data, current_style, severity_scores, edge_data, annotations)
        send_to_github(graph_data)
        return 'Thank you for your donation! Data sent to GitHub.', False

    return 'Donate to send data to GitHub', is_open

# Blur background when information modal is open 
def toggle_blur(donation_modal, color_modal, sizing_modal, inspect_modal, factor_edit, edge_edit):
    if donation_modal or color_modal or sizing_modal or inspect_modal or factor_edit or edge_edit:
        return 'blur'
    return 'no-blur'

# Back-button functionality (un-do changes)
def undo_last_action(n_clicks, history):
    if n_clicks and history:
        # Pop the last state from the history
        last_state = history.pop()

        elements = last_state['elements']
        edit_map_data = last_state['edit_map_data']
        severity_scores = last_state['severity_scores']

        cytoscape_elements = edit_map_data.get('elements', [])
        options_1 = [{'label': element['data'].get('label', element['data'].get('id')), 'value': element['data'].get('id')} for element in cytoscape_elements if 'data' in element and 'label' in element['data'] and 'id' in element['data']]

        return elements, options_1, edit_map_data, severity_scores, history

    # If history is empty, return current state (no change)
    return dash.no_update, dash.no_update, dash.no_update, dash.no_update, history

# Color in edges 
def update_dropdown_on_edge_selection(edge_data, edge_data_store):
    if edge_data:
        edge_id = edge_data['data']['id']
        if edge_data_store and edge_id in edge_data_store:
            return edge_data_store.get(edge_id, None)
    return None

def save_edge_type(n_clicks, edge_data, selected_type, edge_data_store):
    if n_clicks > 0 and edge_data and selected_type:
        edge_id = edge_data['data']['id']
        if edge_data_store is None:
            edge_data_store = {}
        edge_data_store[edge_id] = selected_type
        return edge_data_store
    return edge_data_store

# Open color info modal 
def factor_description_modal(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open

# Register the callbacks
def register_editing_callbacks(app):

    app.callback(
        [Output('edit-map-data', 'data'),
         Output('severity-scores-edit', 'data', allow_duplicate=True)],
        [Input('go-to-edit', 'n_clicks')],
        [State('session-data', 'data'),
         State('severity-scores', 'data')],
         prevent_initial_call=True
    )(load_session_graph)

    app.callback(
        [Output('edit-map-data', 'data', allow_duplicate=True),
         Output('severity-scores-edit', 'data', allow_duplicate=True)],
        [Input('load-map-btn', 'n_clicks')],
        [State('session-data', 'data'),
         State('severity-scores', 'data')],
         prevent_initial_call=True
    )(load_session_graph)

    app.callback(
        Output('download-link', 'data'),
        Input('download-file-btn', 'n_clicks'),
        [State('edit-map-data', 'data'),
        State('severity-scores-edit', 'data'), ##
        State('annotation-data', 'data'),
        State('edge-data', 'data'),
        State('my-mental-health-map', 'stylesheet')],
        prevent_initial_call=True
    )(generate_download)

    app.callback(
        Output('edit-map-data', 'data', allow_duplicate=True),
        Input('upload-data', 'contents'),
        State('upload-data', 'filename'),
        prevent_initial_call=True
    )(upload_graph)

    app.callback(
        [Output('node-edit-modal', 'is_open'),
        Output('modal-node-name', 'value'),
        Output('modal-severity-score', 'value'),
        Output('note-input', 'value')],
        [Input('my-mental-health-map', 'tapNodeData'),
        Input('inspect-switch', 'value'),
        Input('severity-scores-edit', 'data')], ##
        State('annotation-data', 'data'),
        #State('editing-mode', 'data')],  
        prevent_initial_call=True
    )(open_node_edit_modal)

    app.callback(
        Output('my-mental-health-map', 'tapNodeData'),  
        Output('my-mental-health-map', 'tapEdgeData'),
        Input('inspect-switch', 'value'), 
        prevent_initial_call=True
    )(reset_tap_data)

    app.callback(
        Output('annotation-data', 'data'),
        [Input('note-input', 'value')],
        [State('my-mental-health-map', 'tapNodeData'),
        State('annotation-data', 'data')]
    )(update_annotations)

    app.callback(
        [Output('edge-edit-modal', 'is_open'),
        Output('edge-explanation', 'children'),
        Output('edge-strength', 'value'),
        Output('edge-annotation', 'value')],
        [Input('my-mental-health-map', 'tapEdgeData'),
        Input('inspect-switch', 'value')],
        [State('edge-data', 'data'),
         State('language-dropdown', 'value')]
    )(open_edge_edit_modal)

    app.callback(
        [Output('edge-edit-modal', 'is_open', allow_duplicate=True),
         Output('edge-type-dropdown', 'value', allow_duplicate=True)],
        [Input('my-mental-health-map', 'tapEdgeData')],
        [State('inspect-switch', 'value'),
        State('edge-edit-modal', 'is_open'),
        State('edge-data', 'data')],
        prevent_initial_call=True
    )(open_modal_on_edge_tap)

    app.callback(
        [Output('edge-data', 'data', allow_duplicate=True),
        Output('my-mental-health-map', 'stylesheet', allow_duplicate=True),
        Output('edit-map-data', 'data', allow_duplicate=True),
        Output('edge-edit-modal', 'is_open', allow_duplicate=True)],
        [Input('edge-save-btn', 'n_clicks')],
        [State('my-mental-health-map', 'tapEdgeData'),
        State('edge-strength', 'value'),
        State('edge-annotation', 'value'),
        State('edge-data', 'data'),
        State('edit-map-data', 'data'),
        State('my-mental-health-map', 'stylesheet'),
        State('edge-type-dropdown', 'value')],
        prevent_initial_call=True
    )(save_edge_changes_and_close_modal)

    app.callback(
        [Output('my-mental-health-map', 'elements'),
        Output('edit-edge', 'options'),
        Output('edit-map-data', 'data', allow_duplicate=True),
        Output('severity-scores-edit', 'data', allow_duplicate=True), ##
        Output('history-store', 'data'),
        Output('my-mental-health-map', 'stylesheet', allow_duplicate=True)], 
        [Input('btn-plus-node', 'n_clicks')],
        [State('edit-node', 'value'),
        State('my-mental-health-map', 'elements'),
        State('edit-map-data', 'data'),
        State('severity-scores-edit', 'data'), ##
        State('history-store', 'data'),
        State('color_scheme', 'data'),
        State('sizing_scheme', 'data')],  
        prevent_initial_call=True
    )(map_add_node_01)

    app.callback(
        [Output('my-mental-health-map', 'elements', allow_duplicate=True),
        Output('edit-edge', 'options', allow_duplicate=True),
        Output('edit-map-data', 'data', allow_duplicate=True),
        Output('severity-scores-edit', 'data', allow_duplicate=True), ##
        Output('history-store', 'data', allow_duplicate=True),
        Output('my-mental-health-map', 'stylesheet', allow_duplicate=True)],  
        [Input('btn-minus-node', 'n_clicks')],
        [State('edit-node', 'value'),
        State('my-mental-health-map', 'elements'),
        State('edit-map-data', 'data'),
        State('severity-scores-edit', 'data'), ##
        State('history-store', 'data'),
        State('color_scheme', 'data'),
        State('sizing_scheme', 'data')],  
        prevent_initial_call=True
    )(delete_node_01)

    app.callback(
        Output('edit-edge', 'value'),
        Input('edit-edge', 'value')
    )(limit_dropdown_edit_edge)

    app.callback(
        [Output('my-mental-health-map', 'elements', allow_duplicate=True),
        Output('edit-map-data', 'data', allow_duplicate=True),
        Output('history-store', 'data', allow_duplicate=True),
        Output('edge-data', 'data', allow_duplicate=True),
        Output('my-mental-health-map', 'stylesheet', allow_duplicate=True)],
        [Input('btn-plus-edge', 'n_clicks')],
        [State('edit-edge', 'value'),
        State('my-mental-health-map', 'elements'),
        State('edit-map-data', 'data'),
        State('severity-scores-edit', 'data'), ##
        State('history-store', 'data'),
        State('edge-data', 'data'),
        State('color_scheme', 'data'),
        State('sizing_scheme', 'data')],
        prevent_initial_call=True
    )(add_edge_output_01)

    app.callback(
        [Output('my-mental-health-map', 'elements', allow_duplicate=True),
        Output('edit-map-data', 'data', allow_duplicate=True),
        Output('history-store', 'data', allow_duplicate=True),
        Output('edge-data', 'data', allow_duplicate=True)],
        Output('my-mental-health-map', 'stylesheet', allow_duplicate=True),
        [Input('btn-minus-edge', 'n_clicks')],
        [State('edit-edge', 'value'),
        State('my-mental-health-map', 'elements'),
        State('edit-map-data', 'data'),
        State('severity-scores-edit', 'data'), ##
        State('history-store', 'data'),
        State('edge-data', 'data'),
        State('color_scheme', 'data'),
        State('sizing_scheme', 'data')],
        prevent_initial_call=True
    )(delete_edge_output_01)

    app.callback(
        [Output('my-mental-health-map', 'elements', allow_duplicate=True),
        Output('severity-scores-edit', 'data', allow_duplicate=True), ##
        Output('edit-map-data', 'data', allow_duplicate=True),
        Output('my-mental-health-map', 'stylesheet', allow_duplicate=True),
        Output('sizing_scheme', 'data'),
        Output('color_scheme', 'data')],
        [Input('modal-save-btn', 'n_clicks'),
         Input('color-scheme', 'value'),
         Input('sizing-scheme', 'value')],
        [State('modal-node-name', 'value'),
        State('modal-severity-score', 'value'),
        State('my-mental-health-map', 'elements'),
        State('severity-scores-edit', 'data'), ##
        State('edit-map-data', 'data'),
        State('my-mental-health-map', 'tapNodeData')],
        prevent_initial_call=True
    )(save_node_changes_and_apply_schemes)

    app.callback(
        Output('likert-scales-container', 'children'),
        [Input({'type': 'dynamic-dropdown', 'step': 1}, 'value'),
        Input('severity-scores', 'data')] ##
    )(update_likert_scales)

    app.callback(
        Output('severity-scores-edit', 'data'), ##
        [Input({'type': 'likert-scale', 'factor': ALL}, 'value')],
        [State('session-data', 'data'), 
        State('severity-scores-edit', 'data'), ##
        State('edit-map-data', 'data')] 
    )(update_severity_scores)
    
    app.callback(
        Output('custom-color', 'data'),
        Input('custom-node-color', 'value'),
        prevent_initial_call=True
    )(update_custom_color_dropdown)

    app.callback(
        Output('edge-data-store', 'data'),
        Input('save-edge-btn', 'n_clicks'),
        [State('edge-name-input', 'value'),  # Get edge name from input
        State('edge-type-dropdown', 'value'),  # Get selected edge type from dropdown
        State('edge-data-store', 'data')]  # Get current data from store
    )(save_edge_type)

    app.callback(
        Output('my-mental-health-map', 'stylesheet'),
        [Input('my-mental-health-map', 'tapNodeData'),
        Input('inspect-switch', 'value')],
        [State('edit-map-data', 'data')]
        #State('editing-mode', 'data')]
    )(update_stylesheet_01)

    app.callback(
        Output('modal-inspect', 'is_open'),
        [Input('help-inspect', 'n_clicks')],
        [State('modal-inspect', 'is_open')],
    )(inspect_info)

    app.callback(
        Output('modal-color-scheme', 'is_open'),
        [Input('help-color', 'n_clicks')],
        [State('modal-color-scheme', 'is_open')],
    )(toggle_modal_color)

    app.callback(
        Output('modal-color-scheme-body', 'children'),
        [Input('color-scheme', 'value')],
        State('language-dropdown', 'value')
    )(update_modal_content_color)

    app.callback(
        Output('modal-sizing-scheme', 'is_open'),
        [Input('help-size', 'n_clicks')],
        [State('modal-sizing-scheme', 'is_open')],
    )(toggle_modal_sizing)

    app.callback(
        Output('modal-sizing-scheme-body', 'children'),
        [Input('sizing-scheme', 'value')],
        State('language-dropdown', 'value')
    )(update_modal_content_sizing)

    # app.callback(
    #     Output('my-mental-health-map', 'generateImage'),
    #     Input('download-image-btn', 'n_clicks'),
    # )(get_image)

    # app.callback(
    #     Output('download-link', 'data', allow_duplicate=True),  # Assuming an Output of dcc.Download component
    #     Input('download-image-btn', 'n_clicks'),
    #     State('my-mental-health-map', 'generateImage'),
    #     prevent_initial_call=True
    # )(get_image)

    app.callback(
        Output('my-mental-health-map', 'generateImage'),
        Input('download-image-btn', 'n_clicks'),
        prevent_initial_call=True
    )(trigger_image_generation)

    app.callback(
        Output('download-link', 'data', allow_duplicate=True),
        Input('my-mental-health-map', 'imageData'),  # Directly observe imageData
        State('download-image-btn', 'n_clicks'),
        prevent_initial_call=True
    )(get_image)

    app.callback(
        Output('donation-modal', 'is_open'),
        [Input('donate-btn', 'n_clicks')],
        [State('donation-modal', 'is_open')],
    )(donation_modal)

    app.callback(
        [Output('dummy-output', 'children'),
         Output("donation-modal", "is_open", allow_duplicate=True)],
        Input('donation-agree', 'n_clicks'),
        [State('edit-map-data', 'data'),
        State('my-mental-health-map', 'stylesheet'),
        State('severity-scores-edit', 'data'), ##
        State('edge-data', 'data'),
        State('annotation-data', 'data'),
        State("donation-modal", "is_open")],
        prevent_initial_call = True
    )(donate_button_clicked)

    app.callback(
        Output('edit-wrapper', 'className'),
        [Input('donation-modal', 'is_open'),
        Input('modal-color-scheme', 'is_open'),
        Input('modal-sizing-scheme', 'is_open'), 
        Input('modal-inspect', 'is_open'),
        Input('node-edit-modal', 'is_open'),
        Input('edge-edit-modal', 'is_open')],
    )(toggle_blur)

    app.callback(
        [Output('my-mental-health-map', 'elements', allow_duplicate=True),
        Output('edit-edge', 'options', allow_duplicate=True),
        Output('edit-map-data', 'data', allow_duplicate=True),
        Output('severity-scores-edit', 'data', allow_duplicate=True), ##
        Output('history-store', 'data', allow_duplicate=True)],
        [Input('back-btn', 'n_clicks')],
        [State('history-store', 'data')],
        prevent_initial_call=True
    )(undo_last_action)
    
    app.callback(
        Output('edge-type-dropdown', 'value'),
        Input('my-mental-health-map', 'tapEdge'),
        State('edge-type', 'data')
    )(update_dropdown_on_edge_selection)

    app.callback(
        Output('edge-type', 'data'),
        Input('save-edge-btn', 'n_clicks'),
        [State('my-mental-health-map', 'tapEdge'),
        State('edge-type-dropdown', 'value'),
        State('edge-type', 'data')]
    )(save_edge_type)

    app.callback(
        Output('modal-factor-description', 'is_open'),
        [Input('help-factors', 'n_clicks')],
        [State("modal-factor-description", 'is_open')],
    )(factor_description_modal)



