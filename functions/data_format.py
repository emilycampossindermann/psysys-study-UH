import json, base64, requests, os, datetime
from pathlib import Path
from functions.map_style import calculate_degree_centrality
from datetime import datetime
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / '.env')

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

# Send graph file to GitHub
# Returns (success: bool, status_code: int | str)
def send_to_github(data):
    repo_owner = os.environ.get('GITHUB_OWNER', 'emilycampossindermann')
    repo_name = os.environ.get('GITHUB_REPO', 'psysys_app')
    access_token = os.environ.get('GITHUB_TOKEN', '')

    if not access_token:
        print('[GitHub] Token not set. Add GITHUB_TOKEN to your .env file.')
        return False, 'no_token'

    # Safe filename: no slashes or colons
    current_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_path = f"data-donation/graph_{current_date}.json"
    url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}'
    headers = {
        'Authorization': f'token {access_token}',
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28',
    }

    content = json.dumps(data, ensure_ascii=False).encode('utf-8')
    encoded_content = base64.b64encode(content).decode('utf-8')

    payload = {
        'message': f'Map submission {current_date}',
        'content': encoded_content,
    }

    try:
        response = requests.put(url, headers=headers, json=payload, timeout=15)
        # 201 = created, 200 = updated (both are success)
        if response.status_code in (200, 201):
            print(f'[GitHub] Map submitted successfully → {file_path}')
            return True, response.status_code
        else:
            print(f'[GitHub] Submission failed — HTTP {response.status_code}')
            print(f'[GitHub] URL: {url}')
            print(f'[GitHub] Response: {response.text[:500]}')
            return False, response.status_code
    except requests.exceptions.Timeout:
        print('[GitHub] Request timed out after 15 s.')
        return False, 'timeout'
    except requests.exceptions.ConnectionError as e:
        print(f'[GitHub] Connection error: {e}')
        return False, 'connection_error'
    except Exception as e:
        print(f'[GitHub] Unexpected error: {e}')
        return False, 'unknown'