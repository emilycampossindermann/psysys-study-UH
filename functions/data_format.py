import json, base64, requests, datetime
from functions.map_style import calculate_degree_centrality
from datetime import datetime

# Format graph data to export
def format_export_data(data, current_style, severity_scores, edge_data, annotations):
    elements = data.get('elements', [])

    # Calculate & include: degree centralities
    degrees = {element['data']['id']: {'out': 0, 'in': 0} for element in elements if 'id' in element['data']}

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

    current_date = datetime.now().strftime("%y/%m/%d-%H:%M")

    # Ensure the 'edges' key exists in the data, fallback to an empty list if not
    edges = data.get('edges', [])

    # Format data to be exported
    exported_data = {
        'elements': elements,
        'stylesheet': current_style,
        'edges': edges,  # Safely access 'edges'
        'severity-scores': severity_scores,
        'edge-data': edge_data,
        'out-degrees': out_degrees,
        'in-degrees': in_degrees,
        'out-in-ratio': out_in_ratio,
        'annotations': annotations,
        'date': current_date,
        'severity': severity_scores
    }

    return exported_data

# Send graph file to github
def send_to_github(data):
    # Replace with your own GitHub repository details
    repo_owner = 'emilycampossindermann'
    #repo_name = 'PsySys_2.0'
    repo_name = 'psysys_app'
    #current_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    current_date = datetime.now().strftime("%y/%m/%d-%H:%M")
    file_path = f"data-donation/graph_{current_date}.json"
    #access_token = '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'  # Use a secret for production
    access_token = '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'
    url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}'
    headers = {'Authorization': f'token {access_token}'}

    # Encode data to be sent as Base64
    content = json.dumps(data).encode('utf-8')
    encoded_content = base64.b64encode(content).decode('utf-8')

    payload = {
        'message': 'Graph donation',
        'content': encoded_content
    }

    # Make a PUT request to update the file in the repository
    response = requests.put(url, headers=headers, json=payload)

    if response.status_code == 200:
        print('Data sent to GitHub successfully')
    else:
        print('Failed to send data to GitHub')
        print(response.text)