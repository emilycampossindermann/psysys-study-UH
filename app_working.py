from app import app
from constants import factors, hidden_style, visible_style
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import dash
from dash import dcc, html

# app = dash.Dash(
#     __name__,
#     external_stylesheets=[
#         dbc.themes.BOOTSTRAP,
#         'https://use.fontawesome.com/releases/v6.6.0/css/all.css',
#         'assets/styles.css'
#     ],
#     assets_folder='assets',
#     suppress_callback_exceptions=True
# )

# app.title = "PsySys"

server = app.server

# Import callbacks 
from callbacks.layout_callbacks import register_layout_callbacks
from callbacks.editing_callbacks import register_editing_callbacks
from callbacks.comparison_callbacks import register_comparison_callbacks
from constants import translations

register_layout_callbacks(app)
register_editing_callbacks(app)
register_comparison_callbacks(app)

############################################################################################################
## LAYOUT
############################################################################################################
# Layout elements: Next & Back button
button_group = html.Div(
    [
        dbc.Button("Map Editor öffnen",
                   id='go-to-edit',
                   n_clicks=0,
                   style=hidden_style,
                   color="light"),
        html.Span(
            dbc.Button(html.I(className="fas fa-solid fa-angle-right"),
                       id='next-button',
                       n_clicks=0,
                       style=hidden_style,
                       color="light"),
            id='next-btn-wrapper',
            style={'display': 'inline-block'},
        ),
        dbc.Button(html.I(className="fas fa-solid fa-angle-left"), 
                   id='back-button', 
                   n_clicks=0, 
                   style=hidden_style, 
                   color="light"),
    ],
   style={
        'position': 'fixed',
        #'bottom': '70px',
        "bottom": "40px",
        'right': '100px',
        'display': 'flex',
        'flexDirection': 'row-reverse',  # Align buttons to the right
        'gap': '10px',                   # Adds space between the buttons
        'zIndex': '5000',                 # Ensure it's above other content
        "borderRadius": "50px"
    }
)

buttons_map = html.Div(
    [
        dbc.Button("Load from session", id='load', n_clicks=0, style=hidden_style),
        dbc.Button("Upload", id='upload', n_clicks=0, style=hidden_style),
        dbc.Button("Download", id='download', n_clicks=0, style=hidden_style)
    ],
    style={
        'display': 'flex',
        'justifyContent': 'center',  # Centers the buttons horizontally
        'gap': '10px',               # Adds space between the buttons
    }
)

# Layout elements: Navigation sidebar
nav_col = html.Div(
    style={
        "position": "fixed",
        "top": "10px",
        "left": "50%",
        "transform": "translateX(-50%)",
        "width": "85%",
        "max-width": "900px",
        "background": "rgba(255, 255, 255, 0.85)",
        "boxShadow": "0px 4px 10px rgba(0, 0, 0, 0.1)",
        "borderRadius": "15px",
        "padding": "15px 15px",
        "zIndex": 1000,
        "display": "flex",
        "alignItems": "center",
        "justifyContent": "space-between",
        "flexWrap": "wrap",
    },
    children=[
        # Logo (Left-Aligned)
        html.A(
            html.Img(
                src="/assets/logo-clean.png",
                className="glowing-button",
                style={
                    "height": "50px",
                    "width": "50px",
                    "borderRadius": "50%",
                    "objectFit": "cover",
                    "marginLeft": "10px",
                    "transition": "box-shadow 0.3s ease",
                    "cursor": "pointer",
                },
            ),
            href="/",
            className="nav-logo-link",
            style={"textDecoration": "none",
                   "zIndex": "2000"},
        ),

        # Navigation Links (Centered)
        html.Div(
            dbc.Nav(
                [
                    dbc.NavLink(
                        html.Span("Psychoeducation", style={"fontFamily": "Outfit", "color": "black"}),
                        href="/psychoeducation",
                        className="nav-link-custom",
                    ),
                    html.Span(
                        dbc.NavLink(
                            html.Span(id='nav-editor-label', children="Map Editor"),
                            href="/my-mental-health-map",
                            id='nav-editor-link',
                            className="nav-link-custom",
                            style={"fontFamily": "Outfit", "color": "black"},
                        ),
                        id='nav-editor-wrapper',
                        style={'display': 'inline-block'},
                    ),
                    dbc.Tooltip(id='nav-editor-tooltip', target='nav-editor-wrapper', children="", style={'display': 'none'}, autohide=True, delay={"show": 150, "hide": 50}),
                ],
                className="justify-content-center",
            ),
            style={"flex": "1", "textAlign": "center", "marginLeft": "-60px"},
        ),
    ],
)


# Layout elements: Page content
content_col = dbc.Col(
    [
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content'),
        button_group,
        buttons_map
    ],
    md=12,
)

# Layout elements: Translation toggle
translation_toggle = dbc.Col([
    dcc.Dropdown(
        id='language-dropdown',
        className="custom-dropdown",
        options=[
            {
                'label': html.Div([
                    html.Img(
                        src="/assets/us.png",  # Replace with your own US flag path
                        style={
                            "width": "20px",
                            "height": "20px",
                            "borderRadius": "50%",  # Round flag
                            "marginRight": "20px",
                            "marginTop": "7px"
                        }
                    ),
                    #"English"
                ], style={"display": "flex", "alignItems": "center"}),
                'value': 'en'
            },
            {
                'label': html.Div([
                    html.Img(
                        src="/assets/de.png",  # Replace with your own German flag path
                        style={
                            "width": "20px",
                            "height": "20px",
                            "borderRadius": "50%",  # Round flag
                            "marginRight": "20px",
                            "marginTop": "7px"
                        }
                    ),
                    #"Deutsch"
                ], style={"display": "flex", "alignItems": "center"}),
                'value': 'de'
            }
        ],
        value='de',  # Default to English
        clearable=False,
        style={
            'float': 'right',
            #'width': '120px',  # Adjust width to fit flags and text
            "width": '60px',
            'borderRadius': "50px",
            'fontFamily': "Outfit",
            'fontSize': "14px"
        }
    )],
    md=2,
    style={
        'position': 'absolute',
        'top': '15px',
        'right': '60px',
        'textAlign': 'left',
        'padding': '10px',
        'zIndex': '3000',
        'width': '150px'  # Adjust to match dropdown width
    })


# Stylesheet for network 
stylesheet = [{'selector': 'node',
               'style': {'background-color': '#9CD3E1', 
                         'label': 'data(label)', 
                         'font-family': 'Outfit',
                         'text-max-width': '5px'}},
              {'selector': 'edge',
               'style': {'curve-style': 'bezier', 
                         'target-arrow-shape': 'triangle', 
                         'control-point-step-size': '40px' }}
    ]

# Define app layout
app.layout = dbc.Container([
    dbc.Row([nav_col,translation_toggle, content_col]),
    dcc.Store(id="psychoeducation-visited", data={"visited": False}, storage_type='session'),
    dcc.Store(id='dropdown-store', storage_type='memory'),
    dcc.Store(id='history-store', data=[]),
    dcc.Store(id="now-step", data=1, storage_type="session"),
    dcc.Store(id='current-step', data={'step': 0}, storage_type='session'),
    dcc.Store(id='color_scheme', data=None, storage_type='session'),
    dcc.Store(id='edge-type', data=None, storage_type='session'),
    dcc.Store(id='sizing_scheme', data=None, storage_type='session'),
    dcc.Store(id='custom-color', data={}, storage_type='session'),
    html.Div(id='hidden-div', style={'display': 'none'}),
    dcc.Store(id='selected-nodes', data=[]), 
    dcc.Store(id='editing-mode', data=[]),
    dcc.Store(id='plot-mode', data=[]),
    dcc.Store(id='current-filename-store', storage_type='session'),
    dcc.Store(id='session-data', data={
        'dropdowns': {
            'initial-selection': {'options':[{'label': factor, 'value': factor} for factor in factors], 'value': None},
            'chain1': {'options':[], 'value': None},
            'chain2': {'options':[], 'value': None},
            'cycle1': {'options':[], 'value': None},
            'cycle2': {'options':[], 'value': None},
            'target': {'options':[], 'value': None},
            },
        'elements': [], 
        'edges': [],
        'add-nodes': [],
        'add-edges': [],
        'stylesheet': stylesheet,
        'annotations': []
    }, storage_type='session'),
    dcc.Store(id='edit-map-data', data={
        'dropdowns': {
            'initial-selection': {'options':[{'label': factor, 'value': factor} for factor in factors], 'value': None},
            'chain1': {'options':[], 'value': None},
            'chain2': {'options':[], 'value': None},
            'cycle1': {'options':[], 'value': None},
            'cycle2': {'options':[], 'value': None},
            'target': {'options':[], 'value': None},
            },
        'elements': [], 
        'edges': [],
        'add-nodes': [],
        'add-edges': [],
        'stylesheet': stylesheet,
        'annotations': [],
        'severity': {}
    }, storage_type='session'),
    dcc.Store(id='severity-scores', data={}, storage_type='session'),
    dcc.Store(id='severity-scores-edit', data={}, storage_type='session'),
    dcc.Store(id='annotation-data', data={}, storage_type='session'),
    dcc.Store(id='edge-data', data={}, storage_type='session'),
    dcc.Store(id='comparison', data={}, storage_type='session'),
    dcc.Store(id='track-map-data', data={
        'elements': [], 
        'stylesheet': stylesheet,
        'severity': {},
        'timeline-marks': {0: 'PsySys'},
        'timeline-min': 0,
        'timeline-max': 0,
        'timeline-value': 0
        
}, storage_type='session'),
    dcc.Download(id='download-link'),
    dcc.Store(id='video-watched-store', data={}, storage_type='local'),
    # Track whether onboarding pop-ups have been shown this session
    dcc.Store(id='welcome-modal-shown', data=False, storage_type='session'),
    dcc.Store(id='editor-modal-shown', data=False, storage_type='session'),
    html.Div(id='dummy-output', style={'display': 'none'}),
    dbc.Tooltip(id='next-btn-tooltip', target='next-btn-wrapper', placement='top',
                children="", style={'display': 'none'}, autohide=True,
                delay={"show": 150, "hide": 50}),
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle(id='congrats-modal-title'), style={"fontFamily": "Outfit", "fontWeight": 500, "border": "none"}),
        dbc.ModalBody(id='congrats-modal-body', style={"fontFamily": "Outfit", "fontWeight": 300, "fontSize": "18px", "textAlign": "center", "padding": "20px 30px"}),
        # Hidden dummy elements so existing callbacks referencing these IDs don't error
        html.Span(id='congrats-editor-btn', style={"display": "none"}),
        html.Span(id='congrats-editor-btn-text', style={"display": "none"}),
        dbc.Button(id='congrats-close-btn', n_clicks=0, style={"display": "none"}),
        html.Span(id='congrats-close-btn-text', style={"display": "none"}),
    ], id='congrats-modal', is_open=False, centered=True,
       style={"fontFamily": "Outfit", "zIndex": "9000"}),
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("Von vorne beginnen?", style={"fontFamily": "Outfit", "fontWeight": 500})),
        dbc.ModalBody(
            "Deine aktuelle Map wird gelöscht und die Sitzung startet neu. Bist du sicher?",
            style={"fontFamily": "Outfit", "fontWeight": 300, "fontSize": "18px"}
        ),
        dbc.ModalFooter([
            dbc.Button("Ja, neu starten", id="confirm-redo-btn", n_clicks=0,
                       style={"borderRadius": "50px", "fontFamily": "Outfit", "fontWeight": 300,
                              "backgroundColor": "#E57373", "border": "none", "color": "white"}),
            dbc.Button("Abbrechen", id="cancel-redo-btn", n_clicks=0,
                       style={"borderRadius": "50px", "fontFamily": "Outfit", "fontWeight": 300,
                              "marginLeft": "10px", "backgroundColor": "transparent",
                              "border": "2px solid #6F4CFF", "color": "#6F4CFF"}),
        ])
    ], id="redo-confirm-modal", is_open=False,
       style={"fontFamily": "Outfit", "zIndex": "9000"}),

    # ── Welcome pop-up (shown once per session before psychoeducation) ────────
    dbc.Modal([
        dbc.ModalHeader(
            dbc.ModalTitle(id='welcome-modal-title', style={"fontFamily": "Outfit", "fontWeight": 600, "fontSize": "22px"}),
            style={"border": "none", "paddingBottom": "0"}
        ),
        dbc.ModalBody(id='welcome-modal-body', style={"fontFamily": "Outfit", "padding": "10px 28px 20px"}),
        dbc.ModalFooter([
            dbc.Button(id='welcome-modal-close', n_clicks=0, children="Los geht's!",
                style={"borderRadius": "50px", "fontFamily": "Outfit", "fontWeight": 400,
                       "background": "linear-gradient(135deg, #6F4CFF, #AE52FF)",
                       "border": "none", "color": "white", "padding": "10px 28px",
                       "fontSize": "16px"}),
        ], style={"border": "none", "justifyContent": "center", "paddingTop": "0"}),
    ], id='welcome-modal', is_open=False, centered=True,
       style={"fontFamily": "Outfit", "zIndex": "9100"}),

    # ── Editor onboarding pop-up (shown once per session on first editor visit)
    dbc.Modal([
        dbc.ModalHeader(
            dbc.ModalTitle(id='editor-modal-title', style={"fontFamily": "Outfit", "fontWeight": 600, "fontSize": "22px"}),
            style={"border": "none", "paddingBottom": "0"}
        ),
        dbc.ModalBody(id='editor-modal-body', style={"fontFamily": "Outfit", "padding": "10px 28px 20px"}),
        dbc.ModalFooter([
            dbc.Button(id='editor-modal-close', n_clicks=0, children="Verstanden!",
                style={"borderRadius": "50px", "fontFamily": "Outfit", "fontWeight": 400,
                       "background": "linear-gradient(135deg, #6F4CFF, #AE52FF)",
                       "border": "none", "color": "white", "padding": "10px 28px",
                       "fontSize": "16px"}),
        ], style={"border": "none", "justifyContent": "center", "paddingTop": "0"}),
    ], id='editor-modal', is_open=False, centered=True,
       style={"fontFamily": "Outfit", "zIndex": "9100"}),

], fluid=True)


if __name__ == '__main__':
    app.run(debug=True, port=8069)
