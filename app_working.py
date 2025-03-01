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
        dbc.Button(html.I(className="fas fa-edit nav-icon"), 
                   id='go-to-edit', 
                   n_clicks=0, 
                   style=hidden_style, 
                   color="light"),
        dbc.Button(html.I(className="fas fa-solid fa-angle-right"), 
                   id='next-button', 
                   n_clicks=0, 
                   style=hidden_style, 
                   color="light"),
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
                },
            ),
            href="/",
            style={"textDecoration": "none",
                   "zIndex": "2000"},
        ),

        # Navigation Links (Centered)
        html.Div(
            dbc.Nav(
                [
                    # dbc.NavItem(
                    #     dbc.NavLink(
                    #         "About", href="/project-info",
                    #         style={"color": "black", "font-family": "Outfit", "font-size": "18px", "font-weight": "300"}
                    #     )
                    # ),

                    html.Div(
                        className="dropdown-container",
                        children=[
                            dbc.NavLink(
                                [html.Span("Demo", style={"fontFamily": "Outfit", "color":"black"}), html.Span(" ▼", style={"fontSize": "12px", "fontFamily": "Outfit", "color": "black"})],
                                href="/psysys-demo",
                                className="nav-link-custom dropdown-hover",
                            ),
                            html.Div(
                                className="dropdown-content",
                                children=[
                                    html.Div(
                                        className="dropdown-item",
                                        children=[
                                            dbc.NavLink("Psychoeducation", href="/psychoeducation", className="dropdown-link"),
                                            dbc.NavLink("Map Editor", href="/my-mental-health-map", className="dropdown-link"),
                                            dbc.NavLink("Map Tracker", href="/track-my-mental-health-map", className="dropdown-link"),
                                        ],
                                    )
                                ],
                            ),
                        ],
                    ),

                    # dbc.NavItem(
                    #     dbc.NavLink(
                    #         "Output", href="/output",
                    #         style={"color": "black", "font-family": "Outfit", "font-size": "18px", "font-weight": "300"}
                    #     )
                    # ),
                    dbc.NavItem(
                        dbc.NavLink(
                            "Team", href="/about",
                            style={"color": "black", "font-family": "Outfit", "font-size": "18px", "font-weight": "300"}
                        )
                    ),
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
    md=9,
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
    dcc.Store(id="psychoeducation-visited", data={"visited": False}),
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
    html.Div(id='dummy-output', style={'display': 'none'})
], fluid=True)


if __name__ == '__main__':
    app.run_server(debug=True, port=8069)
