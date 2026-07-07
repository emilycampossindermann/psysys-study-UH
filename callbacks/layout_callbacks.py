import dash, json, time

from app import app
from dash import html, Input, Output, State, ALL, MATCH
from constants import factors, stylesheet, hidden_style, visible_style, translations, factor_translation_map, total_steps, steps
from functions.map_build import (map_add_factors, map_add_chains, map_add_cycles)
from functions.map_style import (graph_color)
from functions.page_content import (generate_step_content, create_mental_health_map_tab, create_tracking_tab, create_about,
                                    create_demo_page, create_landing_page, create_learn_more_page, create_output_page, 
                                    create_blog_page, create_thesis_page, create_article_page, create_press_page)

# Translate PsySys factors 

def update_factors_based_on_language(selected_language, session_data, edit_map_data):
    # Initialize dropdowns if they don't exist in session_data or edit_map_data
    session_data['dropdowns'] = session_data.get('dropdowns', {'initial-selection': {'options': [], 'value': []}})
    edit_map_data['dropdowns'] = edit_map_data.get('dropdowns', {'initial-selection': {'options': [], 'value': []}})
    
    # Get the translation dictionary based on the selected language
    translation = translations.get(selected_language, translations['de'])
    
    reverse_translation_map = {v: k for k, v in factor_translation_map.items()}

    # Retrieve current selected factors, defaulting to an empty list if None
    selected_factors = session_data['dropdowns']['initial-selection'].get('value', [])

    # Translate the selected factors
    if selected_language == 'en':
        translated_selected_factors = [reverse_translation_map.get(factor, factor) for factor in selected_factors]
    else:
        translated_selected_factors = [factor_translation_map.get(factor, factor) for factor in selected_factors]

    # Update the dropdown options and selected values
    #options = [{'label': factor, 'value': factor} for factor in translation['factors']]
    options = [{'label': factor, 'value': factor} for factor in translations['de']['factors']]

    # Update session_data and edit_map_data dropdowns
    session_data['dropdowns']['initial-selection']['options'] = options
    session_data['dropdowns']['initial-selection']['value'] = translated_selected_factors

    edit_map_data['dropdowns']['initial-selection']['options'] = options
    edit_map_data['dropdowns']['initial-selection']['value'] = translated_selected_factors

    return session_data, edit_map_data

# Display the page & next/back button based on current step 
def update_page_and_buttons(pathname, edit_map_data, current_step_data, language, session_data, color, sizing,
                            track_data, map_store, custom_color_data, severity_scores, visited_data=None):
    
    step = current_step_data.get('step', 0)  # Default to step 0 if not found

    # Default button states
    content = None
    back_button_style = hidden_style
    next_button_style = visible_style
    redirect_button_style = hidden_style
    next_button_text = html.I(className="fas fa-solid fa-angle-right")
    class_name = ""
    go_to_edit_class = ""

    translation = translations.get(language, translations['de'])
    psysys_complete = step >= 5 or (visited_data or {}).get('visited', False)

    # Update content and button states based on the pathname and step
    if pathname == '/psychoeducation':
        # Check the step and update accordingly
        if step == 0:
            content = generate_step_content(step, session_data, translation)   
            class_name = "button-hover-gradient"
            next_button_text = html.Div("Start", style={"fontFamily": "Outfit", "fontWeight": 300,})  #"backgroundClip": "padding-box", "background": "linear-gradient(to right, #f4f4f9, #d6ccff, #9b84ff, #6F4CFF)"})
        elif step == 1:
            content = generate_step_content(step, session_data, translation)
            class_name = "button-hover-gradient"
            back_button_style = hidden_style  
        elif 2 <= step <= 4:
            content = generate_step_content(step, session_data, translation)
            class_name = "button-hover-gradient"
            back_button_style = visible_style            
            next_button_style = visible_style         
        elif step == 5:
            content = generate_step_content(step, session_data, translation, severity_scores)
            class_name = "button-hover-gradient"
            back_button_style = visible_style
            next_button_style = hidden_style  # hide Redo button on results page
            redirect_button_style = visible_style
            go_to_edit_class = "glowing-button"

    elif pathname == "/my-mental-health-map":
        content = create_mental_health_map_tab(edit_map_data, color, sizing, custom_color_data, translation)
        back_button_style = hidden_style
        next_button_style = hidden_style

    elif pathname == "/track-my-mental-health-map":
        content = create_tracking_tab(track_data, translation)
        back_button_style = hidden_style
        next_button_style = hidden_style

    elif pathname == "/about": # translate
        content = create_about(app, translation)
        back_button_style = hidden_style
        next_button_style = hidden_style

    elif pathname == "/psysys-demo":
        content = create_demo_page(translation, 5 if psysys_complete else step)
        back_button_style = hidden_style
        next_button_style = hidden_style

    elif pathname == "/project-info": # translate
        content = create_learn_more_page(translation)
        back_button_style = hidden_style
        next_button_style = hidden_style

    elif pathname == "/output":
        content = create_output_page(translation)
        back_button_style = hidden_style
        next_button_style = hidden_style

    elif pathname == "/blog":
        content = create_blog_page(translation)
        back_button_style = hidden_style
        next_button_style = hidden_style

    elif pathname == "/thesis":
        content = create_thesis_page(translation)
        back_button_style = hidden_style
        next_button_style = hidden_style

    elif pathname == "/article":
        content = create_article_page(translation)
        back_button_style = hidden_style
        next_button_style = hidden_style

    elif pathname == "/press":
        content = create_press_page(translation)
        back_button_style = hidden_style
        next_button_style = hidden_style

    elif pathname == "/":
        content = create_demo_page(translation, 5 if psysys_complete else step)
        back_button_style = hidden_style
        next_button_style = hidden_style

    elif content is None:
        content = html.Div("Page not found")

    return content, back_button_style, next_button_style, next_button_text, redirect_button_style, class_name, go_to_edit_class

# Update current step based on next/back button clicks
def update_step(back_clicks, next_clicks, current_step_data):
    back_clicks = back_clicks or 0
    next_clicks = next_clicks or 0

    # Use callback_context to determine which input has been triggered
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if "back-button.n_clicks" in changed_id:
        # Decrement the step, ensuring it doesn't go below 0
        current_step_data['step'] = max(current_step_data['step'] - 1, 0)
    elif "next-button.n_clicks" in changed_id:
        if current_step_data['step'] >= 5:
            pass  # Redo is handled by the confirmation modal — do not reset here
        else:
            current_step_data['step'] += 1

    return current_step_data


# Open Redo confirmation modal when "Redo" (next at step 5) is clicked
def open_redo_modal(n_clicks, current_step_data):
    if n_clicks and current_step_data.get('step') == 5:
        return True
    return False


# Confirm Redo: reset to step 0 AND clear video-watched-store so gates apply again
def confirm_redo(n_clicks):
    if n_clicks:
        return {'step': 0}, False, {}
    return dash.no_update, dash.no_update, dash.no_update


# Cancel Redo: close modal without resetting
def cancel_redo(n_clicks, is_open):
    if n_clicks:
        return False
    return is_open


# Disable Next button until video checkbox is checked + step-specific requirements
def gate_next_button(video_watched_store, step_data, session_data, severity_scores):
    step = step_data.get('step', 0) if step_data else 0
    steps_with_videos = [0, 1, 2, 3, 4]  # step 5 is summary, no gate

    if step in steps_with_videos:
        watched = (video_watched_store or {}).get(str(step), False) or (video_watched_store or {}).get(step, False)
        if not watched:
            return True  # disabled — video checkbox not yet checked

    dd = (session_data or {}).get('dropdowns', {})

    # Step 1: between 3 and 7 factors selected, AND all have severity >= 1
    if step == 1:
        selected = dd.get('initial-selection', {}).get('value') or []
        if len(selected) < 3 or len(selected) > 7:
            return True
        scores = severity_scores or {}
        if any(scores.get(f, 0) < 1 for f in selected):
            return True

    # Step 2: both chain dropdowns need at least 2 selections each
    if step == 2:
        chain1 = dd.get('chain1', {}).get('value') or []
        chain2 = dd.get('chain2', {}).get('value') or []
        if len(chain1) < 2 or len(chain2) < 2:
            return True

    # Step 3: both cycle dropdowns need at least 1 selection each
    if step == 3:
        cycle1 = dd.get('cycle1', {}).get('value') or []
        cycle2 = dd.get('cycle2', {}).get('value') or []
        if len(cycle1) < 1 or len(cycle2) < 1:
            return True

    # Step 4: exactly 1 target factor must be selected
    if step == 4:
        target = dd.get('target', {}).get('value')
        # target is a single string (multi=False dropdown)
        if not target or (isinstance(target, list) and len(target) == 0):
            return True

    return False  # enabled


# Mark video as watched when checkbox is checked
def update_video_watched_from_checkbox(check_values, step_ids, current_store):
    store = dict(current_store or {})
    for val, id_dict in zip(check_values or [], step_ids or []):
        if val and 'watched' in val:
            store[id_dict['step']] = True
    return store


# Hide the video checkbox for steps that are already watched (on revisit).
# Step 0 is always kept visible; if already watched, it is pre-checked.
def hide_confirmed_checkboxes(store, step_data, component_ids):
    hidden = {'display': 'none'}
    visible = {"marginTop": "12px", "fontFamily": "Outfit", "fontWeight": 300,
               "fontSize": "15px", "color": "#6F4CFF", "textAlign": "center"}
    styles = []
    values = []
    for id_dict in (component_ids or []):
        step = id_dict['step']
        watched = (store or {}).get(step, False) or (store or {}).get(str(step), False)
        styles.append(hidden if watched else visible)
        values.append(['watched'] if watched else [])
    return styles, values

# Update session data based on user input
def update_hidden_div(values):
    try:
        return json.dumps(values)
    except TypeError:
        return json.dumps(["Serialization error with values"])

def update_session_data(n_clicks, json_values, session_data, current_step_data, severity_scores):
    step = current_step_data.get('step')
    values = json.loads(json_values) if json_values else []

    # Ensure 'dropdowns' and other keys exist in session_data
    session_data.setdefault('dropdowns', {
        'initial-selection': {'options': [], 'value': None},
        'chain1': {'options': [], 'value': None},
        'chain2': {'options': [], 'value': None},
        'cycle1': {'options': [], 'value': None},
        'cycle2': {'options': [], 'value': None},
        'target': {'options': [], 'value': None},
    })

    # Store severity scores
    session_data['severity'] = severity_scores or {}

    # Rest of your logic
    if len(values) == 1:
        if step == 1:
            session_data = map_add_factors(session_data, values[0], severity_scores)

    # Store raw dropdown values immediately (for gating, without requiring n_clicks)
    if len(values) == 1:
        if step == 4:
            session_data['dropdowns']['target']['value'] = values[0]
    if len(values) == 2:
        if step == 2:
            session_data['dropdowns']['chain1']['value'] = values[0] or []
            session_data['dropdowns']['chain2']['value'] = values[1] or []
        elif step == 3:
            session_data['dropdowns']['cycle1']['value'] = values[0] or []
            session_data['dropdowns']['cycle2']['value'] = values[1] or []

    if n_clicks:
        if len(values) == 1:
            if step == 4:
                session_data['dropdowns']['target']['value'] = values[0]
                graph_color(session_data, severity_scores)

        elif len(values) == 2:
            if step == 2:
                session_data = map_add_chains(session_data, values[0], values[1])
            elif step == 3:
                session_data = map_add_cycles(session_data, values[0], values[1])

    # Ensure session_data remains JSON-compatible
    try:
        json.dumps(session_data)
    except TypeError:
        session_data = {"error": "Session data serialization issue"}

    return session_data


# Update session data based on initial factor selection
def dropdown_step5_init(value, session_data):
    if session_data['add-nodes'] == []:
        session_data['add-nodes'] = value
    return session_data

# Reset session data & severity data at "Redo" (step 0)
def reset(current_step_data):
    if current_step_data['step'] == 0:
        data = {
            'dropdowns': {
                'initial-selection': {'options': [{'label': factor, 'value': factor} for factor in factors], 
                                      'value': []},
                'chain1': {'options': [], 'value': None},
                'chain2': {'options': [], 'value': None},
                'cycle1': {'options': [], 'value': None},
                'cycle2': {'options': [], 'value': None},
                'target': {'options': [], 'value': None},
            },
            'elements': [],
            'edges': [],
            'add-nodes': [],
            'add-edges': [],
            'stylesheet': stylesheet,
            'annotations': []
        }
        return (data, {}) 
    else:
        return (dash.no_update, dash.no_update)

# Re-direct user to edit tab & populate graph with PsySys map when user clicks on redirect button end of PsySys
def redirect_edit(n_clicks):
    if n_clicks:
        return "/my-mental-health-map"

# Extract likert scale severity 
def extract_severity_scores(severity_values, current_severity_scores, slider_ids, session_data):
    factor_selection = session_data['dropdowns']['initial-selection']['value']
    
    if factor_selection is None:
        return dash.no_update
    
    if current_severity_scores is None:
        current_severity_scores = {}

    # Ensure severity_values and slider_ids are not None
    if severity_values is None or slider_ids is None:
        return current_severity_scores

    # Remove any factors from current_severity_scores that are not in the Likert scales
    current_severity_scores = {factor: score for factor, score in current_severity_scores.items() if factor in factor_selection}

    # Extract factor names and update their values in the severity scores
    for value, slider_id in zip(severity_values, slider_ids):
        factor = slider_id['factor']  # Extract the factor name from the slider id
        current_severity_scores[factor] = value

    return current_severity_scores

# Show suicide hotline message if user selects thoughts of death or suicide
def show_suicide_prevention_message(selected_factors):
    if 'Thoughts of death or suicide' in (selected_factors or []) or 'Gedanken an den Tod oder Suizid' in (selected_factors or []):
        return {"color": "#516395", "visibility": "visible"}
    return {"color": "#516395", "visibility": "hidden"}

# Limit dropdown for factor selection to 7 (max allowed)
def limit_factor_selection(selection):
    if selection and len(selection) > 7:
        return selection[:7]
    return selection

# Callback for toggling the collapse
def toggle_collapse(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open

def toggle_navbar(n, is_open):
    return not is_open


# Tooltip: step-aware message explaining why Next is disabled
def update_next_btn_tooltip(is_disabled, language, step_data, video_store, session_data, severity_scores):
    if not is_disabled:
        return "", {'display': 'none'}

    de = (language == 'de')
    step = (step_data or {}).get('step', 0)
    watched = (video_store or {}).get(step, False) or (video_store or {}).get(str(step), False)
    dd = (session_data or {}).get('dropdowns', {})
    scores = severity_scores or {}
    reasons = []

    if step in [0, 1, 2, 3, 4] and not watched:
        reasons.append("Schau dir zuerst das Video an." if de else "Watch the video first.")

    if step == 1:
        selected = dd.get('initial-selection', {}).get('value') or []
        if len(selected) < 3:
            reasons.append("Wähle mindestens 3 Faktoren aus." if de else "Select at least 3 factors.")
        elif len(selected) > 7:
            reasons.append("Wähle maximal 7 Faktoren aus." if de else "Select at most 7 factors.")
        elif any(scores.get(f, 0) < 1 for f in selected):
            reasons.append("Gib für alle Faktoren einen Schweregrad an." if de else "Rate the severity for all selected factors.")

    if step == 2:
        chain1 = dd.get('chain1', {}).get('value') or []
        chain2 = dd.get('chain2', {}).get('value') or []
        if len(chain1) < 2 or len(chain2) < 2:
            reasons.append("Wähle mindestens 2 Faktoren in jeder Auswahl." if de
                           else "Select at least 2 factors in each dropdown.")

    if step == 3:
        cycle1 = dd.get('cycle1', {}).get('value') or []
        cycle2 = dd.get('cycle2', {}).get('value') or []
        if len(cycle1) < 1 or len(cycle2) < 1:
            reasons.append("Wähle mindestens 1 Faktor in jeder Auswahl." if de
                           else "Select at least 1 factor in each dropdown.")

    if step == 4:
        target = dd.get('target', {}).get('value')
        if not target:
            reasons.append("Wähle einen Faktor aus der Liste aus." if de else "Select a factor from the dropdown.")

    if not reasons:
        reasons.append("Bitte erfülle alle Bedingungen." if de else "Please complete all requirements.")

    return " ".join(reasons), {}


# Open congrats modal when user reaches step 5 for the first time (only on psychoeducation page)
def open_congrats_modal(step_data, pathname, language):
    step = (step_data or {}).get('step', 0)
    t = translations.get(language or 'de', translations['de'])
    if step == 5 and pathname == '/psychoeducation':
        return (True,
                t.get('congrats_title', 'Congratulations! 🎉'),
                t.get('congrats_body', "You've completed PsySys!"),
                t.get('congrats_editor_btn', 'Open Map Editor'),
                t.get('congrats_close', 'Close'))
    return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update


def close_congrats_modal(n_clicks):
    if n_clicks:
        return False
    return dash.no_update


# Track when PsySys is completed (step reaches 5) — persists within session even if user goes back
def mark_psysys_completed(step_data, visited_data):
    step = (step_data or {}).get('step', 0)
    visited = (visited_data or {}).get('visited', False)
    if step >= 5 or visited:
        return {"visited": True}
    return dash.no_update


# Gate nav editor link based on PsySys completion (step >= 5 OR previously completed)
def update_editor_nav_access(step_data, visited_data, language):
    from dash import html as _html
    step = (step_data or {}).get('step', 0)
    completed = step >= 5 or (visited_data or {}).get('visited', False)
    t = translations.get(language or 'de', translations['de'])
    if not completed:
        tooltip_text = t.get('editor_locked_tooltip', 'Complete PsySys first.')
        link_href = "#"
        link_style = {"pointerEvents": "none", "color": "#aaa", "opacity": "0.5", "fontFamily": "Outfit"}
        tooltip_style = {}
        nav_label = ["Map Editor ", _html.Span("🔒", style={"fontSize": "14px"})]
    else:
        tooltip_text = ""
        link_href = "/my-mental-health-map"
        link_style = {"fontFamily": "Outfit", "color": "black"}
        tooltip_style = {"display": "none"}
        nav_label = "Map Editor"
    return tooltip_text, tooltip_style, link_href, link_style, nav_label


def _build_modal_steps(step_pairs, step_style, num_style, title_style, body_style):
    """Helper: build a list of styled step rows for modal bodies."""
    from dash import html as _h
    rows = []
    for title, body in step_pairs:
        rows.append(_h.Div([
            _h.Div(style={**step_style}, children=[
                _h.P(title, style=title_style),
                _h.P(body, style=body_style),
            ])
        ]))
    return rows


# Open welcome modal every time user visits /psychoeducation
def show_welcome_modal(pathname, already_shown, language):
    from dash import html as _h
    if pathname != '/psychoeducation':
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update
    t = translations.get(language or 'de', translations['de'])
    step_style = {
        "padding": "12px 16px", "marginBottom": "10px",
        "backgroundColor": "rgba(111,76,255,0.06)",
        "borderRadius": "12px",
    }
    title_s = {"fontFamily": "Outfit", "fontWeight": 500, "fontSize": "15px",
                "margin": "0 0 3px 0", "color": "#1a1a2e"}
    body_s  = {"fontFamily": "Outfit", "fontWeight": 300, "fontSize": "14px",
                "margin": "0", "color": "#555"}
    steps = [
        (t.get('welcome_modal_step1_title',''), t.get('welcome_modal_step1_body','')),
        (t.get('welcome_modal_step2_title',''), t.get('welcome_modal_step2_body','')),
        (t.get('welcome_modal_step3_title',''), t.get('welcome_modal_step3_body','')),
    ]
    body = _h.Div([
        _h.P(t.get('welcome_modal_intro',''), style={**body_s, "marginBottom": "14px", "fontSize": "15px"}),
        *_build_modal_steps(steps, step_style, {}, title_s, body_s),
    ])
    btn_label = t.get('welcome_modal_btn', "Los geht's!")
    return True, True, t.get('welcome_modal_title',''), body, btn_label


# Open editor modal every time user visits /my-mental-health-map
def show_editor_modal(pathname, already_shown, language):
    from dash import html as _h
    if pathname != '/my-mental-health-map':
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update
    t = translations.get(language or 'de', translations['de'])
    study_link = "https://sosci.zdv.uni-mainz.de/PECAN_INT/?q=qnr4"
    step_style = {
        "padding": "12px 16px", "marginBottom": "10px",
        "backgroundColor": "rgba(111,76,255,0.06)",
        "borderRadius": "12px",
    }
    title_s = {"fontFamily": "Outfit", "fontWeight": 500, "fontSize": "15px",
                "margin": "0 0 3px 0", "color": "#1a1a2e"}
    body_s  = {"fontFamily": "Outfit", "fontWeight": 300, "fontSize": "14px",
                "margin": "0", "color": "#555"}
    # Build step 3 with styled back-to-study button
    step3_body = _h.Div([
        _h.P(t.get('editor_modal_step3_body',''), style={**body_s, "marginBottom": "8px"}),
        _h.A(
            t.get('submit_back_to_study', '→ Zurück zur Studie'),
            href=study_link,
            target="_blank",
            style={
                "display": "inline-block",
                "padding": "9px 20px",
                "backgroundColor": "#6F4CFF",
                "color": "white",
                "borderRadius": "50px",
                "fontFamily": "Outfit",
                "fontWeight": 600,
                "fontSize": "14px",
                "textDecoration": "none",
                "boxShadow": "0 3px 12px rgba(111,76,255,0.35)",
            }
        ),
    ])
    steps = [
        (t.get('editor_modal_step1_title',''), t.get('editor_modal_step1_body','')),
        (t.get('editor_modal_step2_title',''), t.get('editor_modal_step2_body','')),
    ]
    body = _h.Div([
        *_build_modal_steps(steps, step_style, {}, title_s, body_s),
        _h.Div([
            _h.Div(style={**step_style}, children=[
                _h.P(t.get('editor_modal_step3_title',''), style=title_s),
                step3_body,
            ])
        ]),
    ])
    btn_label = t.get('editor_modal_btn', 'Verstanden!')
    return True, True, t.get('editor_modal_title',''), body, btn_label


# Register the callbacks
def register_layout_callbacks(app):

    app.callback(
        [Output('session-data', 'data', allow_duplicate=True),
        Output('edit-map-data', 'data', allow_duplicate=True)],
        [Input('language-dropdown', 'value')],
        [State('session-data', 'data'),
        State('edit-map-data', 'data')],
        prevent_initial_call=True
    )(update_factors_based_on_language)

    app.callback(
        [Output('page-content', 'children'),
        Output('back-button', 'style'),
        Output('next-button', 'style', allow_duplicate=True),
        Output('next-button', 'children'),
        Output('go-to-edit', 'style'),
        Output('next-button', 'className'),
        Output('go-to-edit', 'className'),],
        [Input('url', 'pathname'),
        Input('edit-map-data', 'data'),
        Input('current-step', 'data'),
        Input('language-dropdown', 'value')],
        [State('session-data', 'data'),
        State('color_scheme', 'data'),
        State('sizing_scheme', 'data'),
        State('track-map-data', 'data'),
        State('comparison', 'data'),
        State('custom-color', 'data'),
        State('severity-scores', 'data'),
        State('psychoeducation-visited', 'data')],
        prevent_initial_call=True
    )(update_page_and_buttons)

    app.callback(
        Output('current-step', 'data'),
        [Input('back-button', 'n_clicks'),
        Input('next-button', 'n_clicks')],
        [State('current-step', 'data')]
    )(update_step)

    app.callback(
        Output('hidden-div', 'children', allow_duplicate=True),
        Input({'type': 'dynamic-dropdown', 'step': ALL}, 'value'),
        prevent_initial_call=True
    )(update_hidden_div)

    app.callback(
        Output('session-data', 'data'),
        [Input('next-button', 'n_clicks'),
        Input('hidden-div', 'children')],
        [State('session-data', 'data'),
        State('current-step', 'data'),
        State('severity-scores', 'data')]
    )(update_session_data)

    app.callback(
        Output('session-data', 'data', allow_duplicate=True),
        Input('factor-dropdown', 'value'),
        State('session-data', 'data'),
        prevent_initial_call=True
    )(dropdown_step5_init)

    app.callback(
        [Output('session-data', 'data', allow_duplicate=True),
        Output('severity-scores', 'data', allow_duplicate=True)],
        Input('current-step', 'data'),
        prevent_initial_call=True
    )(reset)

    app.callback(
         Output('severity-scores', 'data'),  # Update the stored severity scores
        [Input({'type': 'likert-scale', 'factor': ALL}, 'value')],
        [State('severity-scores', 'data'),  # Current severity scores
        State({'type': 'likert-scale', 'factor': ALL}, 'id'), 
        State('session-data', 'data')]  # Get the IDs (factors) of all scales
    )(extract_severity_scores)

    app.callback(
        Output('suicide-prevention-hotline', 'style'),
        [Input({'type': 'dynamic-dropdown', 'step': 1}, 'value')]
    )(show_suicide_prevention_message)

    app.callback(
        Output('url', 'pathname'),
        Input('go-to-edit', 'n_clicks')
    )(redirect_edit)

    app.callback(
        Output({'type': 'dynamic-dropdown', 'step': 1}, 'value'),
        Input({'type': 'dynamic-dropdown', 'step': 1}, 'value')
    )(limit_factor_selection)

    app.callback(
        Output("psysys-demo-collapse", "is_open"),
        [Input("psysys-demo-link", "n_clicks")],
        [dash.dependencies.State("psysys-demo-collapse", "is_open")],
    )(toggle_collapse)

    app.callback(
        Output("navbar-collapse", "is_open"),
        [Input("navbar-toggler", "n_clicks")],
        [dash.State("navbar-collapse", "is_open")],
        prevent_initial_call=True,
    )(toggle_navbar)

    # Redo confirmation modal
    app.callback(
        Output('redo-confirm-modal', 'is_open'),
        Input('next-button', 'n_clicks'),
        State('current-step', 'data'),
        prevent_initial_call=True
    )(open_redo_modal)

    app.callback(
        [Output('current-step', 'data', allow_duplicate=True),
         Output('redo-confirm-modal', 'is_open', allow_duplicate=True),
         Output('video-watched-store', 'data', allow_duplicate=True)],
        Input('confirm-redo-btn', 'n_clicks'),
        prevent_initial_call=True
    )(confirm_redo)

    app.callback(
        Output('redo-confirm-modal', 'is_open', allow_duplicate=True),
        Input('cancel-redo-btn', 'n_clicks'),
        State('redo-confirm-modal', 'is_open'),
        prevent_initial_call=True
    )(cancel_redo)

    # Gate next-button: requires video, 3-7 factors + severity at step 1, chain/cycle at 2-3, target at step 4
    app.callback(
        Output('next-button', 'disabled'),
        Input('video-watched-store', 'data'),
        Input('current-step', 'data'),
        Input('session-data', 'data'),
        Input('severity-scores', 'data'),
    )(gate_next_button)

    # Update video-watched-store when a checkbox is ticked
    app.callback(
        Output('video-watched-store', 'data', allow_duplicate=True),
        Input({'type': 'video-confirm', 'step': ALL}, 'value'),
        State({'type': 'video-confirm', 'step': ALL}, 'id'),
        State('video-watched-store', 'data'),
        prevent_initial_call=True
    )(update_video_watched_from_checkbox)

    # Hide the checkbox for steps already watched (fires on store update or step change)
    # Also pre-fills the value for step 0 if previously watched.
    app.callback(
        [Output({'type': 'video-confirm', 'step': ALL}, 'style'),
         Output({'type': 'video-confirm', 'step': ALL}, 'value')],
        Input('video-watched-store', 'data'),
        Input('current-step', 'data'),
        State({'type': 'video-confirm', 'step': ALL}, 'id'),
        prevent_initial_call=True
    )(hide_confirmed_checkboxes)

    # Tooltip on next button: step-aware hint, hidden when button is enabled
    app.callback(
        [Output('next-btn-tooltip', 'children'),
         Output('next-btn-tooltip', 'style')],
        Input('next-button', 'disabled'),
        State('language-dropdown', 'value'),
        State('current-step', 'data'),
        State('video-watched-store', 'data'),
        State('session-data', 'data'),
        State('severity-scores', 'data'),
    )(update_next_btn_tooltip)

    # Track PsySys completion persistently (even when user navigates back)
    app.callback(
        Output('psychoeducation-visited', 'data'),
        Input('current-step', 'data'),
        State('psychoeducation-visited', 'data'),
        prevent_initial_call=True
    )(mark_psysys_completed)

    app.callback(
        [Output('nav-editor-tooltip', 'children'),
         Output('nav-editor-tooltip', 'style'),
         Output('nav-editor-link', 'href'),
         Output('nav-editor-link', 'style'),
         Output('nav-editor-label', 'children')],
        Input('current-step', 'data'),
        State('psychoeducation-visited', 'data'),
        State('language-dropdown', 'value'),
    )(update_editor_nav_access)

    app.callback(
        [Output('congrats-modal', 'is_open'),
         Output('congrats-modal-title', 'children'),
         Output('congrats-modal-body', 'children'),
         Output('congrats-editor-btn-text', 'children'),
         Output('congrats-close-btn-text', 'children')],
        Input('current-step', 'data'),
        State('url', 'pathname'),
        State('language-dropdown', 'value'),
        prevent_initial_call=True
    )(open_congrats_modal)

    app.callback(
        Output('congrats-modal', 'is_open', allow_duplicate=True),
        Input('congrats-close-btn', 'n_clicks'),
        prevent_initial_call=True
    )(close_congrats_modal)

    # ── Welcome pop-up: open on first /psychoeducation visit, update shown-flag
    app.callback(
        [Output('welcome-modal', 'is_open'),
         Output('welcome-modal-shown', 'data'),
         Output('welcome-modal-title', 'children'),
         Output('welcome-modal-body', 'children'),
         Output('welcome-modal-close', 'children')],
        Input('url', 'pathname'),
        State('welcome-modal-shown', 'data'),
        State('language-dropdown', 'value'),
        prevent_initial_call=True
    )(show_welcome_modal)

    app.callback(
        Output('welcome-modal', 'is_open', allow_duplicate=True),
        Input('welcome-modal-close', 'n_clicks'),
        prevent_initial_call=True
    )(lambda n: False if n else dash.no_update)

    # ── Editor pop-up: open on first /my-mental-health-map visit
    app.callback(
        [Output('editor-modal', 'is_open'),
         Output('editor-modal-shown', 'data'),
         Output('editor-modal-title', 'children'),
         Output('editor-modal-body', 'children'),
         Output('editor-modal-close', 'children')],
        Input('url', 'pathname'),
        State('editor-modal-shown', 'data'),
        State('language-dropdown', 'value'),
        prevent_initial_call=True
    )(show_editor_modal)

    app.callback(
        Output('editor-modal', 'is_open', allow_duplicate=True),
        Input('editor-modal-close', 'n_clicks'),
        prevent_initial_call=True
    )(lambda n: False if n else dash.no_update)


