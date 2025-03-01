# Initiate graph with elements
def map_add_factors(session_data, value, severity_score):
    if value is None:
        value = []

    current_selection = value
    previous_selection = session_data['dropdowns']['initial-selection']['value'] or []

    # Initialize or clear elements list
    session_data['elements'] = []

    if current_selection:
        # Add factor nodes
        for factor in current_selection:
            session_data['elements'].append({'data': {'id': factor, 'label': factor}})

        # Identify factors that are no longer selected
        removed_factors = [factor for factor in previous_selection if factor not in current_selection]

        # Remove these factors from severity data (dictionary)
        for factor in removed_factors:
            if factor in severity_score:
                del severity_score[factor]

        # Update the edges
        if 'edges' in session_data:
            updated_edges = []
            for edge in session_data['edges']:
                source, target = edge.split('->')
                if source in current_selection and target in current_selection:
                    updated_edges.append(edge)
                    # Adding edge elements
                    session_data['elements'].append({'data': {'source': source, 'target': target, 'id': edge}})
            session_data['edges'] = updated_edges

    # Update the previous selection
    session_data['dropdowns']['initial-selection']['value'] = current_selection

    return session_data

# Add an edge 
def add_edge(source, target, elements, existing_edges):
        edge_key = f"{source}->{target}"
        if edge_key not in existing_edges:
            elements.append({'data': {'source': source, 'target': target}})
            existing_edges.add(edge_key)
            return elements, existing_edges
        else:
            return elements, existing_edges
        
# Delete an edge
def delete_edge(source, target, elements, existing_edges):
    # Remove the edge from elements
    elements[:] = [element for element in elements if not ('source' in element.get('data', {}) and element['data']['source'] == source and 'target' in element.get('data', {}) and element['data']['target'] == target)]
    
    # Remove the edge from existing_edges if it's stored as a tuple (source, target)
    existing_edges.discard((source, target))

# Check if a factor exists in elements
def factor_exists(factor, elements):
    return any(element.get('data', {}).get('id') == factor for element in elements)

# Remove chain edges    
def remove_chain_edges(chain, elements, existing_edges, cycles):
    cycle_edges = set()
    for cycle in cycles:
        for i in range(len(cycle) - 1):
            cycle_edges.add((cycle[i], cycle[i + 1]))

    for i in range(len(chain) - 1):
        edge = (chain[i], chain[i + 1])
        # Only remove edge if it's not in any of the cycles
        if edge not in cycle_edges:
            elements[:] = [e for e in elements if not ('source' in e.get('data', {}) and e['data']['source'] == edge[0] and 'target' in e.get('data', {}) and e['data']['target'] == edge[1])]
            existing_edges[:] = [e for e in existing_edges if not ('source' in e.get('data', {}) and e['data']['source'] == edge[0] and e['data']['target'] == edge[1])]

# Add an edge to the elements
def add_edge_new(source, target, elements):
    edge_data = {'data': {'source': source, 'target': target}}
    if not any(e.get('data') == edge_data['data'] for e in elements):
        elements.append(edge_data)

# Add chain elements
def map_add_chains(session_data, chain1, chain2):
    map_elements = session_data['elements']
    previous_chain1 = session_data['dropdowns']['chain1']['value'] or []
    previous_chain2 = session_data['dropdowns']['chain2']['value'] or []
    cycle1 = session_data['dropdowns']['cycle1']['value'] or []
    cycle2 = session_data['dropdowns']['cycle2']['value'] or []

    existing_edges = session_data['edges']

    # Remove previous selections from elements
    for selection in [previous_chain1, previous_chain2]:
        remove_chain_edges(selection, map_elements, existing_edges, [cycle1, cycle2])

    # Process chain1 and chain2
    for chain in [chain1, chain2]:
        if chain is not None:
            for i in range(len(chain) - 1):
                source, target = chain[i], chain[i + 1]
                if factor_exists(source, map_elements) and factor_exists(target, map_elements):
                    add_edge_new(source, target, map_elements)

    session_data['elements'] = map_elements
    session_data['dropdowns']['chain1']['value'] = chain1
    session_data['dropdowns']['chain2']['value'] = chain2
    session_data['edges'] = existing_edges

    return session_data

# Remove cycle edges
def remove_cycle_edges(cycle, elements, existing_edges, chains):
    # Gather all edges from chain1 and chain2
    chain_edges = set()
    for chain in chains:
        if chain:
            for i in range(len(chain) - 1):
                chain_edges.add((chain[i], chain[i + 1]))

    # Remove edges from the cycle if they are not in the chains
    for i in range(len(cycle)):
        source = cycle[i]
        target = cycle[0] if i == len(cycle) - 1 else cycle[i + 1]
        edge = (source, target)

        # Only remove edge if it's not in chain1 or chain2
        if edge not in chain_edges:
            elements[:] = [e for e in elements if not ('source' in e.get('data', {}) and e['data']['source'] == source and 'target' in e.get('data', {}) and e['data']['target'] == target)]
            existing_edges.discard(edge)

# Add cycles
def map_add_cycles(session_data, cycle1, cycle2):
    map_elements = session_data['elements']
    existing_edges = set(session_data['edges'])

    # Get previous cycles
    previous_cycle1 = session_data['dropdowns']['cycle1']['value'] or []
    previous_cycle2 = session_data['dropdowns']['cycle2']['value'] or []

    chain1 = session_data['dropdowns']['chain1']['value'] or []
    chain2 = session_data['dropdowns']['chain2']['value'] or []

    # Remove previous cycles
    for cycle in [previous_cycle1, previous_cycle2]:
        #remove_cycle_edges(cycle, map_elements, existing_edges)
        remove_cycle_edges(cycle, map_elements, existing_edges, [chain1, chain2])

    # Add new cycles
    for cycle in [cycle1, cycle2]:
        if cycle is not None:
            if len(cycle) == 1:
                element = cycle[0]
                if factor_exists(element, map_elements):
                    add_edge_new(element, element, map_elements)
            elif len(cycle) > 1:
                for i in range(len(cycle)):
                    source = cycle[i]
                    target = cycle[0] if i == len(cycle) - 1 else cycle[i + 1]
                    if factor_exists(source, map_elements) and factor_exists(target, map_elements):
                        add_edge_new(source, target, map_elements)

    session_data['elements'] = map_elements
    session_data['edges'] = list(existing_edges)
    session_data['dropdowns']['cycle1']['value'] = cycle1
    session_data['dropdowns']['cycle2']['value'] = cycle2
    
    return session_data
