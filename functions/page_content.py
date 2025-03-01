import dash_bootstrap_components as dbc
import re
import dash_cytoscape as cyto
from dash import dcc, html
from constants import (COMMON_STYLE, HEADER_STYLE, VIDEO_STYLE, VIDEO_CONTAINER_STYLE, TEXT_BLOCK_STYLE, 
                       TEXT_STYLE, CONTENT_CONTAINER_STYLE, ABOUT_MEMBER_STYLE, ABOUT_PARTNER_STYLE, 
                       ABOUT_SECTION_STYLE, IMAGE_STYLE, TEXT_CONTAINER_STYLE, TEXT_ELEMENT_STYLE,
                       EDITING_WINDOW_STYLE, PLOT_WINDOW_STYLE)

# Function: Embed YouTube video 
def create_iframe(src):
    return html.Iframe(
        width="615",
        height="346",
        src=f"{src}?rel=0&modestbranding=1",
        allow="accelerometer;autoplay;clipboard-write;encrypted-media;gyroscope;picture-in-picture;fullscreen"
    )

# Function: Create dropdown menu 
def create_dropdown(id, options, value, placeholder, multi=True):
    return dcc.Dropdown(
        id=id,
        options=options,
        value=value,
        placeholder=placeholder,
        multi=multi,
        style={'width': '100%', "fontFamily": "Outfit", "fontWeight": 200, "fontSize": "16px","borderRadius": "15px"}
    )

# Function: Generate likert scales to indicate factor severity
def create_likert_scale(factor, initial_value=0):
    return html.Div([
        html.Label([
            html.Span('Severity of ',
                      style={"fontFamily": "Outfit",  
                             "fontWeight": 200, 
                             'color': 'black'}),
            html.Span(factor, 
                      style={"fontFamily": "Outfit",  
                             "fontWeight": 500, 
                             'color': 'black'})
        ]),
        dcc.Slider(
            min=0,
            max=10,
            step=1,
            value=initial_value,
            #marks={i: str(i) for i in range(11)},
            marks={
                    i: {
                        "label": str(i),
                        "style": {#"color": "#C9BEE7", 
                            "color": "white",
                            "fontFamily": "Outfit", "fontWeight": 300},
                    }
                    for i in range(11)
                },
            id={'type': 'likert-scale', 
                'factor': factor}
        )
    ],style={#'width': '50%', 
             'width': '95%',
             'margin': '0 auto'})

# Function: Create progress bar
def create_progress_bar(current_step, translation):
    # Define labels directly within the function
    labels = translation['psysys-steps']

    # Circle elements
    progress_circles = []
    for i, label in enumerate(labels):
        completed = i < current_step
        is_current = i == current_step

        progress_circles.append(
            html.Div(
                style={
                    "display": "flex",
                    "flexDirection": "column",
                    "alignItems": "center",
                    "zIndex": "2",  # Ensure circles are above the line
                },
                children=[
                    html.Div(
                        style={
                            "width": "30px",
                            "height": "30px",
                            "borderRadius": "50%",
                            #"background": "linear-gradient(to bottom, #9B84FF, #6F4CFF)" if completed else "#ffffff",
                            "background": "#6F4CFF" if completed else "#ffffff",
                            "border": "2px solid #6F4CFF" if completed or is_current else "#ccc",
                            "display": "flex",
                            "alignItems": "center",
                            "justifyContent": "center",
                            "color": "#ffffff" if completed else "#6F4CFF",
                            "fontWeight": "400",
                            "fontFamily": "Outfit",
                            "boxShadow": "0px 4px 6px rgba(111, 76, 255, 0.3)" if is_current else "none",
                        },
                        children=html.Span("✔" if completed else str(i + 1)),
                    ),
                    html.Div(
                        style={
                            "marginTop": "5px",
                            "color": "#6F4CFF" if is_current else "#999",
                            "fontWeight": "300",
                            "fontFamily": "Outfit",
                            "fontSize": "15px",
                        },
                        children=label,  # Use the predefined label
                    ),
                ],
            )
        )

    # Progress bar container
    return html.Div(
        style={
            "position": "relative",
            "display": "flex",
            "alignItems": "center",
            "justifyContent": "space-between",  # Distribute circles evenly
            "marginLeft": "120px",
            "marginRight": "0px",
            "marginBottom": "20px",
            "maxWidth": "1000px"
        },
        children=[
            # Line connecting the circles
            html.Div(
                style={
                    "position": "absolute",
                    "top": "15px",  # Move the line to the vertical center of the circles
                    "left": "2%",
                    "right": "2%",
                    "height": "4px",
                    "background": "linear-gradient(to right, #d6ccff, #9b84ff, #6F4CFF)" if current_step > 0 else "#ccc",
                    "zIndex": "1",  # Line is behind the circles
                    "borderRadius": "2px",
                }
            ),
            # Add the circles on top of the line
            *progress_circles,
        ],
    )

# Function: Generate step content based on session data
def generate_step_content(step, session_data, translation):
    # Function content
    if step == 0:
        return html.Div(
            html.Div(
                    style={**COMMON_STYLE, 
                            "background": "linear-gradient(to bottom, white, #f4f4f9, #d6ccff, #9b84ff, #6F4CFF)",
                            #"marginLeft": "-12px"
                            },
                    children=[
                        # Header Section

                        html.Div(
                            style={
                                **HEADER_STYLE,
                                "height": "228px"  # Set a consistent height for the empty header
                            }
                        ),

                        html.Div(create_progress_bar(step, translation), style={"marginTop": "-100px"}),

                        #html.Hr(style={"marginLeft": "0px", "width": "90%", "marginTop": "31px"}),
                        html.Hr(style={"marginLeft": "0px", "width": "90%", "marginTop": "70px"}),

                        # Main Content Container
                        html.Div(
                            style={
                                "display": "flex",
                                "flexDirection": "row",
                                "gap": "20px",
                                "alignItems": "flex-start",
                                "padding": "20px",
                                "marginTop": "-25px"
                            },
                            children=[
                                # Left Section: Fixed Text Block and Likert Scales
                                html.Div(
                                    style={
                                        "width": "40%",
                                        "padding": "15px",
                                        #"marginLeft": "100px",
                                        "marginLeft": "0px"
                                    },
                                    children=[
                                        # Exercise Description and Dropdown
                                        html.Div(
                                            style={
                                                "position": "sticky",
                                                "top": "20px",
                                                "zIndex": "10",
                                                "padding": "15px",
                                                "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.1)",
                                                "borderRadius": "8px",
                                                #"backgroundColor": "#F4F3FE",
                                                "backgroundColor": "rgba(255, 255, 255, 0.65)"
                                                #"backgroundColor": "rgba(201, 226, 255, 0.6)",
                                            },
                                            children=[
                                                html.H5(dcc.Markdown(translation["exercise-0"], dangerously_allow_html=True) , style={**TEXT_STYLE, "color": "black"}),
                                                html.Div(style={"height": "10px"}),
                                                html.Ol(
                                                    [
                                                        html.Li(translation['title_block_01'], style={"color": "black", "fontFamily": "Outfit", "fontWeight": 200, "fontSize": "16px"}),
                                                        html.P(translation['description_block_01'], style={"color": "grey", "fontFamily": "Outfit", "fontWeight": 200, "fontSize": "16px"}),
                                                        html.Li(translation['title_block_02'], style={"color": "black", "fontFamily": "Outfit", "fontWeight": 200, "fontSize": "16px"}),
                                                        html.P(translation['description_block_02'], style={"color": "grey", "fontFamily": "Outfit", "fontWeight": 200, "fontSize": "16px"}),
                                                        html.Li(translation['title_block_03'], style={"color": "black", "fontFamily": "Outfit", "fontWeight": 200, "fontSize": "16px"}),
                                                        html.P(translation['description_block_03'], style={"color": "grey", "fontFamily": "Outfit", "fontWeight": 200, "fontSize": "16px"}),
                                                        html.Li(translation['title_block_04'], style={"color": "black", "fontFamily": "Outfit", "fontWeight": 200, "fontSize": "16px"}),
                                                        html.P(translation['description_block_04'], style={"color": "grey", "fontFamily": "Outfit", "fontWeight": 200, "fontSize": "16px"}),
                                                    ],
                                                )
                                            ],
                                        ),
                                    ],
                                ),

                                # Right Section: Video
                                html.Div(
                                    style={
                                        "width": "48.5%",  # Adjusted to align with the left section
                                        "padding": "15px",
                                        "position": "relative",
                                    },
                                    children=[
                                        html.Iframe(
                                            src=translation["video_link_intro"],
                                            style={
                                                **VIDEO_STYLE,
                                                "marginTop": "0px",
                                                "marginLeft": "0px",
                                            },
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
            # html.Div(
            #     style={**COMMON_STYLE, 
            #         "background": "linear-gradient(to bottom, white, #f4f4f9, #d6ccff, #9b84ff, #6F4CFF)",
            #         "overflow": "auto",  # ✅ Allows scrolling if content is cut off
            #         "height": "100vh",  # Ensures full viewport height
            #         "maxHeight": "100vh",
            #     },
            #     children=[
            #         html.Div(style={**HEADER_STYLE, "height": "228px"}),  # Header
            #         html.Div(create_progress_bar(step, translation), style={"marginTop": "-100px"}),
            #         html.Hr(style={"marginLeft": "0px", "width": "90%", "marginTop": "70px"}),

            #         # Main Content Container (Now Scrollable)
            #         html.Div(
            #             style={
            #                 "display": "flex",
            #                 "justifyContent": "center",
            #                 "flexDirection": "column",  # ✅ Ensure stacking on mobile
            #                 "alignItems": "center",
            #                 "gap": "20px",
            #                 "padding": "20px",
            #                 "overflowY": "auto",  # ✅ Allows vertical scrolling inside content
            #                 "maxHeight": "calc(100vh - 300px)",  # Prevents full viewport lock
            #             },
            #             children=[
            #                 dbc.Row(
            #                     style={"width": "100%", "alignItems": "flex-start"},
            #                     children=[
            #                         # Exercise Field
            #                         dbc.Col(
            #                             html.Div(
            #                                 style={
            #                                     "padding": "15px",
            #                                     "borderRadius": "8px",
            #                                     "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.1)",
            #                                     "backgroundColor": "rgba(255, 255, 255, 0.65)",
            #                                 },
            #                                 children=[
            #                                     html.H5(dcc.Markdown(translation["exercise-0"], dangerously_allow_html=True), 
            #                                             style={**TEXT_STYLE, "color": "black"}),
            #                                     html.Div(style={"height": "10px"}),  # Spacer
            #                                     html.Ol(
            #                                         [
            #                                             html.Li(translation['title_block_01'], 
            #                                                     style={"color": "black", "fontFamily": "Outfit", "fontWeight": 200, "fontSize": "16px"}),
            #                                             html.P(translation['description_block_01'], 
            #                                                 style={"color": "grey", "fontFamily": "Outfit", "fontWeight": 200, "fontSize": "16px"}),

            #                                             html.Li(translation['title_block_02'], 
            #                                                     style={"color": "black", "fontFamily": "Outfit", "fontWeight": 200, "fontSize": "16px"}),
            #                                             html.P(translation['description_block_02'], 
            #                                                 style={"color": "grey", "fontFamily": "Outfit", "fontWeight": 200, "fontSize": "16px"}),

            #                                             html.Li(translation['title_block_03'], 
            #                                                     style={"color": "black", "fontFamily": "Outfit", "fontWeight": 200, "fontSize": "16px"}),
            #                                             html.P(translation['description_block_03'], 
            #                                                 style={"color": "grey", "fontFamily": "Outfit", "fontWeight": 200, "fontSize": "16px"}),

            #                                             html.Li(translation['title_block_04'], 
            #                                                     style={"color": "black", "fontFamily": "Outfit", "fontWeight": 200, "fontSize": "16px"}),
            #                                             html.P(translation['description_block_04'], 
            #                                                 style={"color": "grey", "fontFamily": "Outfit", "fontWeight": 200, "fontSize": "16px"}),
            #                                         ],
            #                                     ),
            #                                 ],
            #                             ),
            #                             md=6, xs=11  # ✅ Side-by-side on large screens, stacked on mobile
            #                         ),

            #                         # Video Section
            #                         dbc.Col(
            #                             html.Div(
            #                                 html.Iframe(
            #                                     src=translation["video_link_intro"],
            #                                     style={
            #                                         **VIDEO_STYLE,
            #                                         "width": "94%",  # ✅ Makes it responsive
            #                                         "height": "315px",  # ✅ Keeps correct aspect ratio
            #                                         "borderRadius": "10px",
            #                                     },
            #                                 ),
            #                                 style={
            #                                     "padding": "15px",
            #                                     "position": "relative",
            #                                     "textAlign": "center",  # ✅ Centers the video on mobile
            #                                 },
            #                             ),
            #                             md=6, xs=12  # ✅ Side-by-side on large screens, stacked on mobile
            #                         ),
            #                     ],
            #                 ),
            #             ],
            #         ),
            #     ],
            # )

            )
    

    if step == 1:
        options = session_data.get('dropdowns', {}).get('initial-selection', {}).get('options', [])
        value = session_data.get('dropdowns', {}).get('initial-selection', {}).get('value', [])
        id = {'type': 'dynamic-dropdown', 'step': 1}

        return html.Div(
            html.Div(
                style={**COMMON_STYLE, 
                            "background": "linear-gradient(to bottom, white, #f4f4f9, #d6ccff, #9b84ff, #6F4CFF)",
                            #"marginLeft": "-12px"
                            },
                children=[
                    # Header Section
                    html.Div(
                        html.Div(
                            id="suicide-prevention-hotline",
                            children=[
                                html.P(
                                    translation['suicide-prevention'],
                                    style={
                                        'color': 'black',
                                        'width': '100%',
                                        'marginTop': '160px',
                                        "marginLeft": "-300px",
                                        "fontFamily": "Outfit",
                                        "fontWeight": 300
                                    },
                                ),
                            ],
                            style={
                                'position': 'fixed',
                                'visibility': 'hidden',
                                'zIndex': '1000',
                            },
                        ),
                        style={**HEADER_STYLE, "height": "228px"},
                    ),

                    html.Div(create_progress_bar(step, translation), style={"marginTop": "-100px"}),

                    html.Hr(style={"marginLeft": "0px", "width": "90%", "marginTop": "70px"}),

                    #html.Hr(style={"marginLeft": "100px", "width": "90%", "marginTop": "-10px"}),

                    # Main Content Container
                    html.Div(
                        style={
                            "display": "flex",
                            "flexDirection": "row",
                            "gap": "20px",
                            "alignItems": "flex-start",
                            "padding": "20px",
                            "marginTop": "-25px"
                        },
                        children=[
                            # Left Section: Fixed Text Block and Likert Scales
                            html.Div(
                                style={
                                    "width": "40%",
                                    "padding": "15px",
                                    #"marginLeft": "100px",
                                },
                                children=[
                                    # Exercise Description and Dropdown
                                    html.Div(
                                        style={
                                            "position": "sticky",
                                            "top": "20px",
                                            "zIndex": "10",
                                            #"backgroundColor": "white",
                                            "padding": "15px",
                                            "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.1)",
                                            "borderRadius": "8px",
                                            #"backgroundColor": "#F4F3FE",
                                            "backgroundColor": "rgba(255, 255, 255, 0.65)"
                                            # "backgroundColor": "#e8eefc",
                                            #"backgroundColor": "#f8f9fa"
                                        },
                                        children=[
                                            html.H5(
                                                dcc.Markdown(translation["exercise-1"], dangerously_allow_html=True),
                                                style=TEXT_STYLE,
                                            ),
                                            html.Div(style={"height": "10px"}),
                                            html.Div(
                                                create_dropdown(
                                                id=id,
                                                options=options,
                                                value=value,
                                                placeholder=translation["placeholder_dd_01"],
                                            ),
                                            className="dynamic-dropdown",
                                            style={'width': "90%"}
                                            ),
                                            dbc.Button(
                                                [html.I(className="fas fa-solid fa-question")], 
                                                id='help-factors', 
                                                color="light", 
                                                className='delete-button',
                                                style={
                                                    'border': '2px solid #6F4CFF', 
                                                    'padding' : '3px 10px 3px 10px',
                                                    'borderRadius': "50px",
                                                    #'color': 'grey', 
                                                    "backgroundColor": "transparent",
                                                    "color": "#6F4CFF",
                                                    "boxShadow": "0px 4px 8px rgba(0, 0, 0, 0.1)",
                                                    'position': 'absolute', 'top': '87px', 'right': '15px', 'zIndex': '10'
                                                }
                                            ),

                                            dbc.Tooltip(
                                                translation['factor-description-btn'],
                                                target='help-factors',  # Matches the button id
                                                placement="top",
                                                autohide=True, 
                                                delay={"show": 200, "hide": 100}
                                            ),

                                            dbc.Modal(
                                                [
                                                    dbc.ModalHeader(
                                                        dbc.ModalTitle(translation['factor_description']),  # Replace with translation if needed
                                                        style={"fontFamily": "Outfit", "fontWeight": 500, "fontSize": "22px"},
                                                    ),
                                                    dbc.ModalBody(
                                                        html.Div(
                                                            style={
                                                                "fontFamily": "Outfit",
                                                                "fontWeight": 300,
                                                                "fontSize": "18px",
                                                                "lineHeight": "1.6",
                                                                "width": "100%",
                                                                "overflowY": "auto",  # Enable vertical scrolling
                                                                "maxHeight": "80vh", 
                                                            },
                                                            children=[
                                                                # Anxiety description
                                                                html.Div(
                                                                    children=[
                                                                        html.Span((translation['factors'][0],": "), style={"fontWeight": 500}),
                                                                        translation["anxiety-description"]
                                                                    ],
                                                                    style={"marginBottom": "20px"},  # Space after Factor 1
                                                                ),
                                                                # Changes in appetite description
                                                                html.Div(
                                                                    children=[
                                                                        html.Span((translation['factors'][1],": "), style={"fontWeight": 500}),
                                                                        translation["changes-appetite-description"]
                                                                    ],
                                                                    style={"marginBottom": "20px"},  # Space after Factor 1
                                                                ),
                                                                # Concentration problems description
                                                                html.Div(
                                                                    children=[
                                                                        html.Span((translation['factors'][2],": "), style={"fontWeight": 500}),
                                                                        translation["concentration-problems-description"]
                                                                    ],
                                                                    style={"marginBottom": "20px"},  # Space after Factor 1
                                                                ),
                                                                # Fear of the future description
                                                                html.Div(
                                                                    children=[
                                                                        html.Span((translation['factors'][3],": "), style={"fontWeight": 500}),
                                                                        translation["fear-of-future-description"]
                                                                    ],
                                                                    style={"marginBottom": "20px"},  # Space after Factor 1
                                                                ),
                                                                # Guilt description
                                                                html.Div(
                                                                    children=[
                                                                        html.Span((translation['factors'][4],": "), style={"fontWeight": 500}),
                                                                        translation["guilt-description"]
                                                                    ],
                                                                    style={"marginBottom": "20px"},  # Space after Factor 1
                                                                ),
                                                                # Hopelessness description
                                                                html.Div(
                                                                    children=[
                                                                        html.Span((translation['factors'][5],": "), style={"fontWeight": 500}),
                                                                        translation["hopelessness-description"]
                                                                    ],
                                                                    style={"marginBottom": "20px"},  # Space after Factor 1
                                                                ),
                                                                # Interpersonal problems description
                                                                html.Div(
                                                                    children=[
                                                                        html.Span((translation['factors'][6],": "), style={"fontWeight": 500}),
                                                                        translation["interpersonal-problems-description"]
                                                                    ],
                                                                    style={"marginBottom": "20px"},  # Space after Factor 1
                                                                ),
                                                                # Irritability description
                                                                html.Div(
                                                                    children=[
                                                                        html.Span((translation['factors'][7],": "), style={"fontWeight": 500}),
                                                                        translation["irritability-description"]
                                                                    ],
                                                                    style={"marginBottom": "20px"},  # Space after Factor 1
                                                                ),
                                                                # Loss of interest description
                                                                html.Div(
                                                                    children=[
                                                                        html.Span((translation['factors'][8],": "), style={"fontWeight": 500}),
                                                                        translation["loss-of-interest-description"]
                                                                    ],
                                                                    style={"marginBottom": "20px"},  # Space after Factor 1
                                                                ),
                                                                # Loss of motivation description
                                                                html.Div(
                                                                    children=[
                                                                        html.Span((translation['factors'][9],": "), style={"fontWeight": 500}),
                                                                        translation["loss-of-motivation-description"]
                                                                    ],
                                                                    style={"marginBottom": "20px"},  # Space after Factor 1
                                                                ),
                                                                # Overthinking description
                                                                html.Div(
                                                                    children=[
                                                                        html.Span((translation['factors'][10],": "), style={"fontWeight": 500}),
                                                                        translation["overthinking-description"]
                                                                    ],
                                                                    style={"marginBottom": "20px"},  # Space after Factor 1
                                                                ),
                                                                # Physical pain description
                                                                html.Div(
                                                                    children=[
                                                                        html.Span((translation['factors'][11],": "), style={"fontWeight": 500}),
                                                                        translation["physical-pain-description"]
                                                                    ],
                                                                    style={"marginBottom": "20px"},  # Space after Factor 1
                                                                ),
                                                                # Procrastination description
                                                                html.Div(
                                                                    children=[
                                                                        html.Span((translation['factors'][12],": "), style={"fontWeight": 500}),
                                                                        translation["procrastination-description"]
                                                                    ],
                                                                    style={"marginBottom": "20px"},  # Space after Factor 1
                                                                ),
                                                                # Reduced activity description
                                                                html.Div(
                                                                    children=[
                                                                        html.Span((translation['factors'][13],": "), style={"fontWeight": 500}),
                                                                        translation["reduced-activity-description"]
                                                                    ],
                                                                    style={"marginBottom": "20px"},  # Space after Factor 1
                                                                ),
                                                                # Sadness description
                                                                html.Div(
                                                                    children=[
                                                                        html.Span((translation['factors'][14],": "), style={"fontWeight": 500}),
                                                                        translation["sadness-description"]
                                                                    ],
                                                                    style={"marginBottom": "20px"},  # Space after Factor 1
                                                                ),
                                                                # Self-blame description
                                                                html.Div(
                                                                    children=[
                                                                        html.Span((translation['factors'][15],": "), style={"fontWeight": 500}),
                                                                        translation["self-blame-description"]
                                                                    ],
                                                                    style={"marginBottom": "20px"},  # Space after Factor 1
                                                                ),
                                                                # Self-neglect description
                                                                html.Div(
                                                                    children=[
                                                                        html.Span((translation['factors'][16],": "), style={"fontWeight": 500}),
                                                                        translation["self-neglect-description"]
                                                                    ],
                                                                    style={"marginBottom": "20px"},  # Space after Factor 1
                                                                ),
                                                                # Shame description
                                                                html.Div(
                                                                    children=[
                                                                        html.Span((translation['factors'][17],": "), style={"fontWeight": 500}),
                                                                        translation["shame-description"]
                                                                    ],
                                                                    style={"marginBottom": "20px"},  # Space after Factor 1
                                                                ),
                                                                # Sleep problems description
                                                                html.Div(
                                                                    children=[
                                                                        html.Span((translation['factors'][18],": "), style={"fontWeight": 500}),
                                                                        translation["sleep-problems-description"]
                                                                    ],
                                                                    style={"marginBottom": "20px"},  # Space after Factor 1
                                                                ),
                                                                # Social isolation description
                                                                html.Div(
                                                                    children=[
                                                                        html.Span((translation['factors'][19],": "), style={"fontWeight": 500}),
                                                                        translation["social-isolation-description"]
                                                                    ],
                                                                    style={"marginBottom": "20px"},  # Space after Factor 1
                                                                ),
                                                                # Stress description
                                                                html.Div(
                                                                    children=[
                                                                        html.Span((translation['factors'][20],": "), style={"fontWeight": 500}),
                                                                        translation["stress-description"]
                                                                    ],
                                                                    style={"marginBottom": "20px"},  # Space after Factor 1
                                                                ),
                                                                # Substance abuse description
                                                                html.Div(
                                                                    children=[
                                                                        html.Span((translation['factors'][21],": "), style={"fontWeight": 500}),
                                                                        translation["substance-abuse-description"]
                                                                    ],
                                                                    style={"marginBottom": "20px"},  # Space after Factor 1
                                                                ),
                                                                # Suicidal thoughts description
                                                                html.Div(
                                                                    children=[
                                                                        html.Span((translation['factors'][22],": "), style={"fontWeight": 500}),
                                                                        translation["suicidal-description"]
                                                                    ],
                                                                    style={"marginBottom": "20px"},  # Space after Factor 1
                                                                ),
                                                                # Tiredness description
                                                                html.Div(
                                                                    children=[
                                                                        html.Span((translation['factors'][23],": "), style={"fontWeight": 500}),
                                                                        translation["tiredness-description"]
                                                                    ],
                                                                    style={"marginBottom": "20px"},  # Space after Factor 1
                                                                ),
                                                                # Worry description
                                                                html.Div(
                                                                    children=[
                                                                        html.Span((translation['factors'][24],": "), style={"fontWeight": 500}),
                                                                        translation["worry-description"]
                                                                    ],
                                                                    style={"marginBottom": "20px"},  # Space after Factor 1
                                                                ),
                                                            ],
                                                        )
                                                    ),
                                                ],
                                                id="modal-factor-description",
                                                is_open=False,
                                                backdrop=True,
                                                #size="lg",  # Larger size for the modal
                                                style={
                                                    #"maxWidth": "80%",  # Adjust the width of the modal
                                                    #"margin": "0 auto",  
                                                    "fontFamily": "Outfit",
                                                    "fontWeight": 300,
                                                    "fontSize": "18px",
                                                    "borderRadius": "15px",  # Optional: Rounded corners for the modal
                                                    "boxShadow": "0px 4px 10px rgba(0, 0, 0, 0.1)",  # Subtle shadow for depth
                                                },
                                            )

                                        ],
                                    ),
                                    html.Br(),

                                    # Likert Scales Section
                                    html.Div(
                                        id="likert-scales-container",
                                        style={
                                            "marginTop": "0px",
                                            "overflowY": "auto",
                                            "maxHeight": "240px",
                                            "padding": "5px",
                                            #"backgroundColor": "#f8f9fa",
                                            "backgroundColor": "transparent",
                                            #"borderRadius": "8px",
                                            #"boxShadow": "0 2px 4px rgba(0, 0, 0, 0.1)",
                                        },
                                    ),
                                ],
                            ),

                            # Right Section: Video
                            html.Div(
                                style={
                                    "width": "48.5%",  # Adjusted to align with the left section
                                    "padding": "15px",
                                    "position": "relative",
                                },
                                children=[
                                    html.Iframe(
                                        src=translation["video_link_block_01"],
                                        style={
                                            **VIDEO_STYLE,
                                            "marginTop": "0px",
                                            "marginLeft": "0px",
                                        },
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
        )


    if step == 2:
        selected_factors = session_data.get('dropdowns', {}).get('initial-selection', {}).get('value', [])
        options = [{'label': factor, 'value': factor} for factor in selected_factors]
        value_chain1 = session_data.get('dropdowns', {}).get('chain1', {}).get('value', [])
        value_chain2 = session_data.get('dropdowns', {}).get('chain2', {}).get('value', [])
        id_chain1 = {'type': 'dynamic-dropdown', 
                     'step': 2}
        id_chain2 = {'type': 'dynamic-dropdown', 
                     'step': 3}
                     
        return html.Div(
            style={**COMMON_STYLE, 
                            "background": "linear-gradient(to bottom, white, #f4f4f9, #d6ccff, #9b84ff, #6F4CFF)",
                            #"marginLeft": "-12px"
                            },
            children=[
                # Header with Welcome Message
                 html.Div(
                    style={
                        **HEADER_STYLE,
                        "height": "228px"  # Set a consistent height for the empty header
                    }
                ),

                html.Div(create_progress_bar(step, translation), style={"marginTop": "-100px"}),

                #html.Hr(style={"marginLeft": "0px", "width": "90%", "marginTop": "31px"}),
                html.Hr(style={"marginLeft": "0px", "width": "90%", "marginTop": "70px"}),

                html.Div(
                    style={
                        "display": "flex",
                        "flexDirection": "row",
                        "gap": "20px",
                        "alignItems": "flex-start",
                        "padding": "20px",
                        "marginTop": "-25px"
                    },
                    children=[
                        # Left Section: Fixed Text Block and Likert Scales
                        html.Div(
                            style={
                                "width": "40%",
                                "padding": "15px",
                                #"marginLeft": "100px",
                            },
                            children=[
                                # Exercise Description and Dropdown
                                html.Div(
                                    style={
                                        "position": "sticky",
                                        "top": "20px",
                                        "zIndex": "10",
                                        #"backgroundColor": "white",
                                        "padding": "15px",
                                        "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.1)",
                                        "borderRadius": "8px",
                                        #"backgroundColor": "#F4F3FE",
                                        "backgroundColor": "rgba(255, 255, 255, 0.65)"
                                        # "backgroundColor": "#e8eefc",
                                        #"backgroundColor": "#f8f9fa"
                                    },
                                    children=[
                                        html.H5(dcc.Markdown(translation["exercise-2"], dangerously_allow_html=True),
                                                style=TEXT_STYLE,
                                                ),
                                        html.Div(style={"height": "10px"}),
                                        html.Div(
                                            create_dropdown(
                                            id=id_chain1,
                                            options=options,
                                            value=value_chain1,
                                            placeholder=translation["placeholder_dd_02"],
                                        ),
                                        className="dynamic-dropdown",
                                        ),
                                        html.Div(style={"height": "10px"}),
                                        html.P(translation["example-2-1"], 
                                            style={'width': '100%',
                                                'fontFamily': 'Outfit',
                                                "fontWeight": "200", 
                                                'color': 'grey',
                                                'fontSize': '16px'}),
                                        html.Div(style={"height": "10px"}),
                                        html.Div(
                                            create_dropdown(
                                            id=id_chain2,
                                            options=options,
                                            value=value_chain2,
                                            placeholder=translation["placeholder_dd_02"],
                                        ),
                                        className="dynamic-dropdown",
                                        ),
                                        html.Div(style={"height": "10px"}),
                                        html.P(translation['example-2-2'], 
                                            style={'width': '100%',
                                                'fontFamily': 'Outfit',
                                                "fontWeight": "200", 
                                                'color': 'grey',
                                                'fontSize': '16px'}),
                                    ],
                                ),
                            ],
                        ),

                        # Right Section: Video
                        html.Div(
                            style={
                                "width": "48.5%",  # Adjusted to align with the left section
                                "padding": "15px",
                                "position": "relative",
                            },
                            children=[
                                html.Iframe(
                                    src=translation["video_link_block_02"],
                                    style={
                                        **VIDEO_STYLE,
                                        "marginTop": "0px",
                                        "marginLeft": "0px",
                                    },
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        )
    
    
    if step == 3:
        selected_factors = session_data.get('dropdowns', {}).get('initial-selection', {}).get('value', [])
        options = [{'label': factor, 'value': factor} for factor in selected_factors]
        value_cycle1 = session_data.get('dropdowns', {}).get('cycle1', {}).get('value', [])
        value_cycle2 = session_data.get('dropdowns', {}).get('cycle2', {}).get('value', [])
        id_cycle1 = {'type': 'dynamic-dropdown', 
                     'step': 4}
        id_cycle2 = {'type': 'dynamic-dropdown', 
                     'step': 5}
        return html.Div(
            style={**COMMON_STYLE, 
                            "background": "linear-gradient(to bottom, white, #f4f4f9, #d6ccff, #9b84ff, #6F4CFF)",
                            #"marginLeft": "-12px"
                            },
            children=[
                # Header with Welcome Message
                 html.Div(
                    style={
                        **HEADER_STYLE,
                        "height": "228px"  # Set a consistent height for the empty header
                    }
                ),

                html.Div(create_progress_bar(step, translation), style={"marginTop": "-100px"}),

                #html.Hr(style={"marginLeft": "100px", "width": "90%", "marginTop": "31px"}),
                html.Hr(style={"marginLeft": "0px", "width": "90%", "marginTop": "70px"}),

                #html.Hr(style={"marginLeft": "100px", "width": "90%", "marginTop": "-10px"}),

                html.Div(
                    style={
                        "display": "flex",
                        "flexDirection": "row",
                        "gap": "20px",
                        "alignItems": "flex-start",
                        "padding": "20px",
                        "marginTop": "-25px"
                    },
                    children=[
                        # Left Section: Fixed Text Block and Likert Scales
                        html.Div(
                            style={
                                "width": "40%",
                                "padding": "15px",
                                #"marginLeft": "100px",
                            },
                            children=[
                                # Exercise Description and Dropdown
                                html.Div(
                                    style={
                                        "position": "sticky",
                                        "top": "20px",
                                        "zIndex": "10",
                                        #"backgroundColor": "white",
                                        "padding": "15px",
                                        "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.1)",
                                        "borderRadius": "8px",
                                        #"backgroundColor": "#F4F3FE",
                                        "backgroundColor": "rgba(255, 255, 255, 0.65)"
                                        # "backgroundColor": "#e8eefc",
                                        #"backgroundColor": "#f8f9fa"
                                    },
                                    children=[
                                        html.H5(dcc.Markdown(translation["exercise-3"], dangerously_allow_html=True),
                                                style=TEXT_STYLE,
                                                ),
                                        html.Div(style={"height": "10px"}),
                                        html.Div(
                                            create_dropdown(
                                            id=id_cycle1,
                                            options=options,
                                            value=value_cycle1,
                                            placeholder=translation["placeholder_dd_03"],
                                        ),
                                        className="dynamic-dropdown",
                                        ),
                                        html.Div(style={"height": "10px"}),
                                        html.P(translation['example-3-1'], 
                                            style={'width': '100%',
                                                'fontFamily': 'Outfit',
                                                "fontWeight": "200", 
                                                'color': 'grey',
                                                'fontSize': '16px'}),
                                        html.Div(style={"height": "10px"}),
                                        html.Div(
                                            create_dropdown(
                                            id=id_cycle2,
                                            options=options,
                                            value=value_cycle2,
                                            placeholder=translation["placeholder_dd_03"],
                                        ),
                                        className="dynamic-dropdown",
                                        ),
                                        html.Div(style={"height": "10px"}),
                                        html.P(translation['example-3-2'], 
                                            style={'width': '100%',
                                                'fontFamily': 'Outfit',
                                                "fontWeight": "200", 
                                                'color': 'grey',
                                                'fontSize': '16px'}),
                                    ],
                                ),
                            ],
                        ),

                        # Right Section: Video
                        html.Div(
                            style={
                                "width": "48.5%",  # Adjusted to align with the left section
                                "padding": "15px",
                                "position": "relative",
                            },
                            children=[
                                html.Iframe(
                                    src=translation["video_link_block_03"],
                                    style={
                                        **VIDEO_STYLE,
                                        "marginTop": "0px",
                                        "marginLeft": "0px",
                                    },
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        )
    
    if step == 4:
        selected_factors = session_data.get('dropdowns', {}).get('initial-selection', {}).get('value', [])
        options = [{'label': factor, 'value': factor} for factor in selected_factors]
        value_target = session_data.get('dropdowns', {}).get('target', {}).get('value', [])
        id = {'type': 'dynamic-dropdown', 
              'step': 6}
        return html.Div(
            style={**COMMON_STYLE, 
                            "background": "linear-gradient(to bottom, white, #f4f4f9, #d6ccff, #9b84ff, #6F4CFF)",
                            #"marginLeft": "-12px"
                            },
            children=[
                # Header with Welcome Message
                 html.Div(
                    style={
                        **HEADER_STYLE,
                        "height": "228px"  # Set a consistent height for the empty header
                    }
                ),

                html.Div(create_progress_bar(step, translation), style={"marginTop": "-100px"}),

                #html.Hr(style={"marginLeft": "100px", "width": "90%", "marginTop": "31px"}),
                html.Hr(style={"marginLeft": "0px", "width": "90%", "marginTop": "70px"}),

                html.Div(
                    style={
                        "display": "flex",
                        "flexDirection": "row",
                        "gap": "20px",
                        "alignItems": "flex-start",
                        "padding": "20px",
                        "marginTop": "-25px"
                    },
                    children=[
                        # Left Section: Fixed Text Block and Likert Scales
                        html.Div(
                            style={
                                "width": "40%",
                                "padding": "15px",
                                #"marginLeft": "100px",
                            },
                            children=[
                                # Exercise Description and Dropdown
                                html.Div(
                                    style={
                                        "position": "sticky",
                                        "top": "20px",
                                        "zIndex": "10",
                                        #"backgroundColor": "white",
                                        "padding": "15px",
                                        "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.1)",
                                        "borderRadius": "8px",
                                        #"backgroundColor": "#F4F3FE",
                                        "backgroundColor": "rgba(255, 255, 255, 0.65)"
                                        # "backgroundColor": "#e8eefc",
                                        #"backgroundColor": "#f8f9fa"
                                    },
                                    children=[
                                        html.H5(dcc.Markdown(translation["exercise-4"], dangerously_allow_html=True),
                                                style=TEXT_STYLE,
                                                ),
                                        html.Div(style={"height": "10px"}),
                                        html.Div(
                                            create_dropdown(
                                            id=id,
                                            options=options,
                                            value=value_target,
                                            placeholder=translation["placeholder_dd_04"],
                                        ),
                                        className="dynamic-dropdown",
                                        ),
                                        html.Div(style={"height": "10px"}),
                                        html.P(translation['example_block_04'], 
                                            style={'width': '100%',
                                                'fontFamily': 'Outfit',
                                                "fontWeight": "200", 
                                                'color': 'grey',
                                                'fontSize': '16px'}),
                                    ],
                                ),
                            ],
                        ),

                        # Right Section: Video
                        html.Div(
                            style={
                                "width": "48.5%",  # Adjusted to align with the left section
                                "padding": "15px",
                                "position": "relative",
                            },
                            children=[
                                html.Iframe(
                                    src=translation["video_link_block_04"],
                                    style={
                                        **VIDEO_STYLE,
                                        "marginTop": "0px",
                                        "marginLeft": "0px",
                                    },
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        )
    
    
    if step == 5:
        elements = session_data.get('elements', [])
        selected_factors = session_data.get('add-nodes', [])
        options = [{'label': factor, 'value': factor} for factor in selected_factors]
        return html.Div(
            style={**COMMON_STYLE, 
                            "background": "linear-gradient(to bottom, white, #f4f4f9, #d6ccff, #9b84ff, #6F4CFF)",
                            #"marginLeft": "-12px"
                            },
            children=[
                # Header Section

                html.Div(
                    style={
                        **HEADER_STYLE,
                        "height": "228px"  # Set a consistent height for the empty header
                    }
                ),

                html.Div(create_progress_bar(step, translation), style={"marginTop": "-100px"}),

                #html.Hr(style={"marginLeft": "100px", "width": "90%", "marginTop": "31px"}),
                html.Hr(style={"marginLeft": "0px", "width": "90%", "marginTop": "70px"}),

                # Main Content Container
                html.Div(
                    style={
                        "display": "flex",
                        "flexDirection": "row",
                        "gap": "20px",
                        "alignItems": "flex-start",
                        "padding": "20px",
                        "marginTop": "-25px"
                    },
                    children=[
                        # Left Section: Fixed Text Block and Likert Scales
                        html.Div(
                            style={
                                "width": "40%",
                                "padding": "15px",
                                #"marginLeft": "100px",
                            },
                            children=[
                                # Exercise Description and Dropdown
                                html.Div(
                                    style={
                                        "position": "sticky",
                                        "top": "20px",
                                        "zIndex": "10",
                                        "padding": "15px",
                                        "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.1)",
                                        "borderRadius": "8px",
                                        #"backgroundColor": "#F4F3FE",
                                        "backgroundColor": "rgba(255, 255, 255, 0.65)"
                                    },
                                    children=[
                                        html.H5(dcc.Markdown(translation["feedback_text"], dangerously_allow_html=True), style={**TEXT_STYLE, "color": "black"}),
                                        html.Div(style={"height": "10px"}),
                                        html.Ol(
                                            [
                                                html.Li(translation['feedback_question_01'], style={"color": "black", "fontFamily": "Outfit", "fontWeight": 200, "fontSize": "15px"}),
                                                html.Li(translation['feedback_question_02'], style={"color": "black", "fontFamily": "Outfit", "fontWeight": 200, "fontSize": "15px"}),
                                                html.Li(translation['feedback_question_03'], style={"color": "black", "fontFamily": "Outfit", "fontWeight": 200, "fontSize": "15px"}),
                                                html.Li(translation['feedback_question_04'], style={"color": "black", "fontFamily": "Outfit", "fontWeight": 200, "fontSize": "15px"}),
                                            ],
                                        )
                                    ],
                                ),
                            ],
                        ),

                        # Right Section: Video
                        html.Div(
                            style={
                                "width": "48.5%",  # Adjusted to align with the left section
                                "padding": "15px",
                                "position": "relative",
                            },
                            children=[
                                cyto.Cytoscape(
                                    id='graph-output',
                                    #elements=session_data['elements'],
                                    elements = elements,
                                    layout={'name': 'cose', 
                                            "padding": 10, 
                                            "nodeRepulsion": 3500,
                                            "idealEdgeLength": 10, 
                                            "edgeElasticity": 5000,
                                            "nestingFactor": 1.2,
                                            "gravity": 1,
                                            "numIter": 1000,
                                            "initialTemp": 200,
                                            "coolingFactor": 0.95,
                                            "minTemp": 1.0,
                                            'fit': True
                                            },
                                    zoom=1,
                                    pan={'x': 200, 'y': 200},
                                    stylesheet = session_data.get('stylesheet', []),
                                    style={**VIDEO_STYLE, "marginLeft": "0px", "marginTop": "0px"}
                                ), 

                                html.Div(
                                    [
                                        html.I(className="fas fa-magnifying-glass-plus"),  # Font Awesome Zoom Icon
                                        html.I(className="fas fa-hand-pointer", style={"margin-left": "10px"}),  # Click Icon
                                    ],
                                    style={
                                        "position": "absolute",
                                        "top": "25px",  # Position at bottom-right of graph
                                        "right": "25px",
                                        "font-size": "20px",  # Make it visible
                                        "color": "#888",  # Subtle gray
                                        "background": "rgba(255, 255, 255, 0.7)",  # Light background
                                        "padding": "5px 10px",
                                        "border-radius": "10px",
                                        "box-shadow": "0 2px 5px rgba(0, 0, 0, 0.2)",  # Soft shadow
                                        "z-index": "1000",
                                        "cursor": "pointer",
                                        },
                                    ),
                            ],
                        ),
                    ],
                ),
            ],
        )
    
    else:
        return None
    

# Function: Create my-mental-health-map editing tab
def create_mental_health_map_tab(edit_map_data, color_scheme_data, sizing_scheme_data, custom_color_data, translation):   
    cytoscape_elements = edit_map_data.get('elements', [])
    options_1 = [{'label': element['data'].get('label', element['data'].get('id')), 
                  'value': element['data'].get('id')} for element in cytoscape_elements if 'data' in element and 'label' in element['data'] and 'id' in element['data']]
    color_schemes = [{'label': color, 'value': color} for color in translation['schemes']]
    sizing_schemes = [{'label': size, 'value': size} for size in translation['schemes']]
    return html.Div(
        style={**COMMON_STYLE, 
               "background": "linear-gradient(to bottom, white, #f4f4f9, #d6ccff, #9b84ff, #6F4CFF)",
               #"marginLeft": "-12px"
               },
            children=[
                # Header with Welcome Message
                html.Div(
                    #style=HEADER_STYLE,
                    children=[
                        html.H2(
                            translation['edit-map-title_01'],
                            style={"fontFamily": "Outfit", 
                                   #"fontWeight": "normal", 
                                   #"color": "black", 
                                   "fontSize": "36px",
                                   "color": "#4A4A8D",
                                   "fontWeight": 500,
                                   "textAlign": "center",
                                   "marginLeft": "-150px",
                                   "marginTop": "-95px"},
                        ),
                    ],
                ),

                html.Hr(style={"marginLeft": "0px", "width": "90%", "marginTop": "40px"}),

                # Main content container (text and video)
                html.Div(
                    style={**CONTENT_CONTAINER_STYLE},
                    children=[
                        # Plot section with question mark button
                        
                        
                                        html.Br(),
                                        html.Br(),
                                        html.Div([
                                            html.Div([
                                                html.Div(translation['edit-text'],
                                                         style=TEXT_STYLE),
                                                html.Div(style={"height":"20px"}),
                                                html.Div([
                                                    dbc.Input(id='edit-node',
                                                              type='text', 
                                                              placeholder=translation['placeholder_enter_factor'], 
                                                              style={'marginRight': '10px', 
                                                                     'borderRadius': '50px',
                                                                     'fontFamily': "Outfit",
                                                                     "fontWeight": 300,
                                                                     'fontSize': '17px'}),
                                                    dbc.Button([
                                                        html.I(
                                                            className="fas fa-solid fa-plus")], 
                                                            id='btn-plus-node', 
                                                            color="primary", 
                                                            className='delete-button',
                                                            style={'border': 'none',
                                                                   #'color': '#8793c9',
                                                                   'color': 'white',
                                                                    #'backgroundColor': 'lightgray', 
                                                                    'backgroundColor': "#A7DCA7",
                                                                    'marginLeft':'8px',
                                                                    "borderRadius": "50px",
                                                                    "boxShadow": "0px 4px 8px rgba(0, 0, 0, 0.1)",}),
                                                    dbc.Button([
                                                        html.I(className="fas fa-solid fa-minus")], 
                                                                id='btn-minus-node', 
                                                                color="danger", 
                                                                className='delete-button',
                                                                style={'border': 'none',
                                                                        'color': 'white',
                                                                        'backgroundColor': '#F4A3A3', 
                                                                        'marginLeft':'8px',
                                                                        "borderRadius": "50px",
                                                                        "boxShadow": "0px 4px 8px rgba(0, 0, 0, 0.1)",})
                                                        ], style={'display': 'flex', 
                                                                  'alignItems': 'right', 
                                                                  'marginBottom': '10px'}),

                                                        html.Div([
                                                            dcc.Dropdown(id='edit-edge', 
                                                                         options=options_1, 
                                                                         placeholder=translation['placeholder_enter_connection'], 
                                                                         multi=True, 
                                                                         style={'width': '96%', 
                                                                                'borderRadius': '50px',
                                                                                'fontFamily': "Outfit",
                                                                                "fontWeight": 300,
                                                                                'fontSize': '17px'}),
                                                            dbc.Button([
                                                                html.I(className="fas fa-solid fa-plus")], 
                                                                       id='btn-plus-edge', 
                                                                       color="primary",
                                                                       className='delete-button',
                                                                       style={'border': 'none',
                                                                              #'color': '#8793c9',
                                                                              'color': 'white',
                                                                              #'backgroundColor': 'lightgray',
                                                                              'backgroundColor': "#A7DCA7",
                                                                              'marginLeft':'8px',
                                                                              "borderRadius": "50px",
                                                                              'padding': '7px 12px',
                                                                              "boxShadow": "0px 4px 8px rgba(0, 0, 0, 0.1)",}),
                                                            dbc.Button([
                                                                html.I(className="fas fa-solid fa-minus")], 
                                                                       id='btn-minus-edge', 
                                                                       color="danger", 
                                                                       className='delete-button',
                                                                       style={'border': 'none',
                                                                              #'color': '#8793c9',
                                                                              'color': 'white',
                                                                              #'backgroundColor': 'lightgray', 
                                                                              'backgroundColor': '#F4A3A3',
                                                                              'marginLeft':'8px',
                                                                              "borderRadius": "50px",
                                                                              'padding': '7px 12px',
                                                                              "boxShadow": "0px 4px 8px rgba(0, 0, 0, 0.1)",}),
                                                        ], style={'display': 'flex', 
                                                                  'alignItems': 'center', 
                                                                  'marginBottom': '10px'}),
                                                    
                                                        html.Div([
                                                            dcc.Dropdown(id='color-scheme', 
                                                                         options=color_schemes, 
                                                                         value=color_scheme_data, 
                                                                         placeholder=translation['placeholder_color_scheme'], 
                                                                         multi=False, 
                                                                         style={'width': '96%', 
                                                                                #'borderRadius': '10px'
                                                                                "borderRadius": "50px",
                                                                                'fontFamily': "Outfit",
                                                                                "fontWeight": 300,
                                                                                'fontSize': '17px'}),
                                                            dbc.Button([
                                                                html.I(className="fas fa-solid fa-question")], 
                                                                       id='help-color', 
                                                                       color="light", 
                                                                       className='delete-button',
                                                                       style={#'border': 'none',
                                                                              "backgroundColor": "transparent",
                                                                              "color": "#6F4CFF",
                                                                              "border": "2px solid #6F4CFF",
                                                                              #'color': 'grey', 
                                                                              'marginLeft':'8px',
                                                                              "borderRadius": "50px",
                                                                               'padding' : '3px 10px 3px 10px',
                                                                               "boxShadow": "0px 4px 8px rgba(0, 0, 0, 0.1)",}),
                                                            dbc.Modal([
                                                                dbc.ModalHeader(
                                                                    dbc.ModalTitle(translation['color_modal_title'])),
                                                                    dbc.ModalBody("", 
                                                                                  id='modal-color-scheme-body')
                                                                    ], 
                                                                    id="modal-color-scheme",
                                                                    backdrop = "False", 
                                                                    style={"display": "flex", 
                                                                           "gap": "5px", 
                                                                           'zIndex':'8000',
                                                                           'fontFamily': "Outfit",
                                                                           "fontWeight": 300,
                                                                           'fontSize': '18px'}),
                                                        ], style={'display': 'flex', 
                                                                  'alignItems': 'center', 
                                                                  'marginBottom': '10px', 
                                                                  'zIndex':'8000'}),

                                                        html.Div([
                                                            dcc.Dropdown(id='sizing-scheme', 
                                                                         options=sizing_schemes, 
                                                                         value=sizing_scheme_data, 
                                                                         placeholder=translation['placeholder_sizing_scheme'], 
                                                                         multi=False,
                                                                         style={'width': '96%', 
                                                                                #'borderRadius': '10px'
                                                                                "borderRadius": "50px",
                                                                                'fontFamily': "Outfit",
                                                                                "fontWeight": 300,
                                                                                'fontSize': '17px'}),
                                                            dbc.Button([
                                                                html.I(className="fas fa-solid fa-question")], 
                                                                       id='help-size', 
                                                                       color="light", 
                                                                       className='delete-button',
                                                                       style={
                                                                            #   'border': 'none',
                                                                            #   'color': 'grey', 
                                                                              "backgroundColor": "transparent",
                                                                              "color": "#6F4CFF",
                                                                              "border": "2px solid #6F4CFF",
                                                                              'marginLeft':'8px',
                                                                              "borderRadius": "50px",
                                                                               'padding' : '3px 10px 3px 10px',
                                                                               "boxShadow": "0px 4px 8px rgba(0, 0, 0, 0.1)",}),
                                                            dbc.Modal([
                                                                dbc.ModalHeader(
                                                                    dbc.ModalTitle(translation['sizing_modal_title'])),
                                                                    dbc.ModalBody("", 
                                                                                  id='modal-sizing-scheme-body')
                                                                    ], 
                                                                    id="modal-sizing-scheme", 
                                                                    style={"display": "flex", 
                                                                           "gap": "5px", 
                                                                           'zIndex':'8000',
                                                                           'fontFamily': "Outfit",
                                                                           "fontWeight": 300,
                                                                           'fontSize': '18px'}),
                                                        ], style={'display': 'flex', 
                                                                  'alignItems': 'center', 
                                                                  'marginBottom': '10px', 
                                                                  'zIndex':'8000'}),
                                                        html.Br(),

                                                        html.Div([
                                                            dbc.Checklist(
                                                                options=[{"label": html.Span(html.I(className="fas fa-magnifying-glass"),style={'color': '#8793c9'}), 
                                                                          "value": 0}],
                                                                value=[1],
                                                                id="inspect-switch",
                                                                switch=True),
                                                            dbc.Button([
                                                                html.I(
                                                                    className="fas fa-solid fa-question")], 
                                                                    id='help-inspect', 
                                                                    color="light", 
                                                                    className='delete-button',
                                                                    style={
                                                                        #    'border': 'none',
                                                                        #    'color': 'grey', 
                                                                            "backgroundColor": "transparent",
                                                                            "color": "#6F4CFF",
                                                                            "border": "2px solid #6F4CFF",
                                                                           'marginLeft':'8px',
                                                                           'borderRadius': '50px',
                                                                           'padding' : '3px 10px 3px 10px',
                                                                           "boxShadow": "0px 4px 8px rgba(0, 0, 0, 0.1)",}),
                                                            dbc.Modal([
                                                                dbc.ModalHeader(
                                                                    dbc.ModalTitle(translation['inspect_modal_title'])),
                                                                    dbc.ModalBody(translation['inspect_modal_text'], 
                                                                                  id='modal-inspect-body')
                                                                    ], 
                                                                    id="modal-inspect", 
                                                                    style={"display": "flex",
                                                                           "gap": "5px", 
                                                                           'zIndex':'8000',
                                                                           'fontFamily': "Outfit",
                                                                            "fontWeight": 300,
                                                                            'fontSize': '18px'}
                                                                           ),
                                                                    ], style={'display': 'flex', 
                                                                              'alignItems': 'center', 
                                                                              'marginBottom': '10px', 
                                                                              'zIndex':'8000'}),
                                                                    
                                                        html.Div([
                                                            dbc.Button([
                                                                html.I(
                                                                    className="fas fa-solid fa-backward")], 
                                                                    id='back-btn', 
                                                                    color="light",
                                                                    className='delete-button', 
                                                                    style={'marginTop': '-32px',
                                                                           'marginLeft': '70px',
                                                                            "backgroundColor": "#6F4CFF",
                                                                            "color": "white",
                                                                            #"border": "2px solid #6F4CFF",
                                                                            "border": "none",
                                                                           'borderRadius': '50px',
                                                                            'padding' : '7px 11px 7px 11px',
                                                                            "boxShadow": "0px 4px 8px rgba(0, 0, 0, 0.1)",}),
                                                            
                                                            dbc.Tooltip(
                                                                translation['hover-back-edit'],
                                                                target='back-btn',  # Matches the button id
                                                                placement="top",
                                                                autohide=True, 
                                                                delay={"show": 500, "hide": 100}
                                                            ),
                                                        ], 
                                                        style={'display': 'flex', 
                                                                  'alignItems': 'center', 
                                                                  'marginTop': '55px', 
                                                                  'marginLeft': '365px'}),
                                                        
                                                        ]), 

                                                    ], 
                                                    id = 'editing-window', 
                                                    style={'width': '500px', 
                                                           'height':"auto", 
                                                           'padding': '10px', 
                                                           'marginTop': '-0px', 
                                                           'marginLeft':'-290px', 
                                                           'backgroundColor': 'white', 
                                                           'borderRadius': '15px', 
                                                           'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)', 
                                                           'zIndex': '2000',
                                                           #"backgroundColor": "rgba(201, 226, 255, 0.4)",
                                                           "backgroundColor": "rgba(255, 255, 255, 0.65)"}),

                        # Cytoscape graph section with vertically stacked controls
                        html.Div(
                            style={
                                "width": "48.5%",  # Adjusted to align with the left section
                                "height": "50%",
                                "padding": "15px",
                                "position": "relative",
                                "marginLeft": "-150px",
                                "marginTop": "-10px"
                            },
                            children=[
                                cyto.Cytoscape(
                                    id='my-mental-health-map',
                                    elements=edit_map_data['elements'],
                                    layout={'name': 'cose', 
                                            "padding": 10,
                                            "nodeRepulsion": 3500,
                                            "idealEdgeLength": 10, 
                                            "edgeElasticity": 5000,
                                            "nestingFactor": 1.2,
                                            "gravity": 1,
                                            "numIter": 1000,
                                            "initialTemp": 200,
                                            "coolingFactor": 0.95,
                                            "minTemp": 1.0,
                                            'fit': True},
                                            zoom=1,
                                            pan={'x': 200, 'y': 200},
                                            stylesheet=edit_map_data['stylesheet'] + [
                                                           {
                                                                "selector": "node",
                                                                "style": {
                                                                    "font-family": "Outfit",
                                                                    "label": "data(label)",
                                                                    "text-halign": "center",
                                                                    "text-valign": "center",
                                                                    "font-size": "14px",
                                                                    "color": "#333333",  # Adjust text color if needed
                                                                },
                                                            },
                                                            {
                                                                "selector": "edge",
                                                                "style": {
                                                                    "font-family": "Outfit",
                                                                    "font-size": "12px",
                                                                    "text-opacity": 1,
                                                                    "text-background-opacity": 0,
                                                                    "text-background-color": "#ffffff",
                                                                },
                                                            },
                                                            {
                                                                "selector": "label",
                                                                "style": {
                                                                    "font-family": "Outfit",
                                                                    "font-size": "16px",
                                                                    "font-weight": "300",
                                                                },
                                                            },
                                                        ],
                                            style={**VIDEO_STYLE, "marginLeft": "-140px"},
                                            generateImage={'type': 'jpg', 'action': 'store'},
                                            ), 
                                html.Div(
                                    [
                                        html.I(className="fas fa-magnifying-glass-plus"),  # Font Awesome Zoom Icon
                                        html.I(className="fas fa-hand-pointer", style={"margin-left": "10px"}),  # Click Icon
                                    ],
                                    style={
                                        "position": "absolute",
                                        "top": "15px",  # Position at bottom-right of graph
                                        "right": "165px",
                                        "font-size": "20px",  # Make it visible
                                        "color": "#888",  # Subtle gray
                                        "background": "rgba(255, 255, 255, 0.7)",  # Light background
                                        "padding": "5px 10px",
                                        "border-radius": "10px",
                                        "box-shadow": "0 2px 5px rgba(0, 0, 0, 0.2)",  # Soft shadow
                                        "z-index": "1000",
                                        "cursor": "pointer",
                                        },
                                    ),

                                html.Div(
                                    style={'display': 'flex', 'justifyContent': 'center', 'gap': '10px', 
                                           'marginTop': '40px', "marginLeft": "-300px"},
                                    children=[
                                        dbc.Button([
                                            html.I(
                                                className="fas fa-solid fa-upload"), " ","PsySys Map"], 
                                                id='load-map-btn',
                                                #className="me-2", 
                                                className='delete-button',
                                                style={'border': 'none',
                                                        #'color': '#8793c9',
                                                       'color': "white",
                                                        #'backgroundColor': 'lightgray',
                                                        #"backgroundColor": "#6F4CFF",
                                                        #"background": 'linear-gradient(90deg, #9B84FF, #6F4CFF, #5738C8)',
                                                        "backgroundColor": "transparent",
                                                        "border": "2px solid white",
                                                        #"border": "none",
                                                        'fontFamily': "Outfit",
                                                        'fontWeight': 300,
                                                        "borderRadius": "50px",
                                                        "boxShadow": "0px 4px 8px rgba(0, 0, 0, 0.1)",
                                                        }),
                                        
                                        dcc.Upload(
                                                id='upload-data',
                                                children= dbc.Button([
                                                    html.I(
                                                        className="fas fa-solid fa-upload"), " ", "file"], 
                                                        color="secondary", 
                                                        id='upload-map-btn',
                                                        className='delete-button',
                                                        style={'border': 'none',
                                                            #    'color': '#8793c9',
                                                            #    'backgroundColor': 'lightgray', 
                                                               'padding': '7px',
                                                               'color': "white",
                                                                #'backgroundColor': 'lightgray',
                                                                #"backgroundColor": "#6F4CFF",
                                                                "backgroundColor": "transparent",
                                                                "border": "2px solid white",
                                                                #"background": 'linear-gradient(90deg, #9B84FF, #6F4CFF, #5738C8)',
                                                                #"border": "none",
                                                                'fontFamily': "Outfit",
                                                                'fontWeight': 300,
                                                                "borderRadius": "50px",
                                                                "boxShadow": "0px 4px 8px rgba(0, 0, 0, 0.1)",}),
                                                style={
                                                    'display': 'inline-block',
                                                },
                                            ),
                                            
                                            dbc.Button([
                                                html.I(
                                                    className="fas fa-solid fa-download"), " ","file"], 
                                                    id='download-file-btn',
                                                    className='delete-button',
                                                    style={'border': 'none',
                                                        #    'color': '#8793c9',
                                                        #    'backgroundColor': 'lightgray', 
                                                           'marginLeft':'8px',
                                                           'color': "white",
                                                            #'backgroundColor': 'lightgray',
                                                            "backgroundColor": "#6F4CFF",
                                                            #"background": 'linear-gradient(90deg, #9B84FF, #6F4CFF, #5738C8)',
                                                            #"border": "none",
                                                            "backgroundColor": "transparent",
                                                            "border": "2px solid white",
                                                            'fontFamily': "Outfit",
                                                            'fontWeight': 300,
                                                            "borderRadius": "50px",
                                                            "boxShadow": "0px 4px 8px rgba(0, 0, 0, 0.1)",}),
                                            dbc.Button([
                                                html.I(
                                                    className="fas fa-solid fa-download"), " ","image"], 
                                                    className='delete-button',
                                                    id='download-image-btn',
                                                    style={'border': 'none',
                                                        #    'color': '#8793c9',
                                                        #    'backgroundColor': 'lightgray', 
                                                           'marginLeft':'8px', 
                                                           'marginRight':'8px',
                                                           'color': "white",
                                                            #'backgroundColor': 'lightgray',
                                                            "backgroundColor": "#6F4CFF",
                                                            #"background": 'linear-gradient(90deg, #9B84FF, #6F4CFF, #5738C8)',
                                                            "backgroundColor": "transparent",
                                                            "border": "2px solid white",
                                                            'fontFamily': "Outfit",
                                                            'fontWeight': 300,
                                                            "borderRadius": "50px",
                                                            "boxShadow": "0px 4px 8px rgba(0, 0, 0, 0.1)",
                                                            #"border": "none"
                                                            }),

                                            dbc.Button(
                                                [
                                                    html.I(className="fas fa-solid fa-hand-holding-medical"),
                                                    " Donate"  # Optional: Include text next to the icon for clarity
                                                ], 
                                                id="donate-btn", 
                                                style={
                                                    "borderRadius": "50px",  # Fully rounded corners
                                                    "background": "linear-gradient(90deg, #6F4CFF, #9B84FF)",  # Distinct purple gradient
                                                    "border": "none",  # No border
                                                    "color": "white",  # White text/icon for contrast
                                                    "padding": "10px 20px",  # Balanced padding for icon and optional text
                                                    "fontSize": "16px",  # Slightly larger text/icon size for emphasis
                                                    "boxShadow": "0px 4px 8px rgba(0, 0, 0, 0.1)",  # Subtle shadow for depth
                                                    "transition": "transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out"  # Smooth hover effects
                                                },
                                                className='delete-button',
                                                n_clicks=0  # Optional: initialize with zero clicks
                                            ),


                                            # Tooltips 
                                            dbc.Tooltip(
                                                translation['hover-load-psysys'],
                                                target='load-map-btn',  # Matches the button id
                                                placement="top",
                                                autohide=True, 
                                                delay={"show": 500, "hide": 100}
                                            ),

                                            dbc.Tooltip(
                                                translation['hover-upload-map'],
                                                target='upload-map-btn',  # Matches the button id
                                                placement="top",
                                                autohide=True, 
                                                delay={"show": 500, "hide": 100}
                                            ),

                                            dbc.Tooltip(
                                                translation['hover-download-map'],
                                                target='download-file-btn',  # Matches the button id
                                                placement="top",
                                                autohide=True, 
                                                delay={"show": 500, "hide": 100}
                                            ),

                                            dbc.Tooltip(
                                                translation['hover-save-image'],
                                                target='download-image-btn',  # Matches the button id
                                                placement="top",
                                                autohide=True, 
                                                delay={"show": 500, "hide": 100}
                                            ),

                                            dbc.Tooltip(
                                                translation['hover-donate'],
                                                target='donate-btn',  # Matches the button id
                                                placement="top",
                                                autohide=True, 
                                                delay={"show": 500, "hide": 100}
                                            ),

                                            # Modals
                                            dbc.Modal([
                                                dbc.ModalHeader(
                                                dbc.ModalTitle(translation['factor_edit_title'])),
                                                    dbc.ModalBody([
                                                        html.Div(translation['factor_edit_name']),
                                                        dbc.Input(id='modal-node-name', 
                                                                type='text'),
                                                        html.Br(),
                                                        html.Div(translation['factor_edit_severity']),
                                                        dcc.Slider(id='modal-severity-score', 
                                                                min=0, 
                                                                max=10, 
                                                                step=1),
                                                        html.Br(),
                                                        #    html.Div("Color:"),
                                                        #    dcc.Dropdown(id='custom-node-color', options=["blue", "purple", "yellow", "green", "red", "orange"], value=None, placeholder='Select a custom color', multi=False, style={'width': '70%', 'borderRadius': '10px'}),
                                                        #    html.Br(),
                                                        html.Div(translation['note']),
                                                        dcc.Textarea(
                                                            id='note-input',
                                                            value='',
                                                            className='custom-textarea',
                                                            style={
                                                                'flex': '1',  # Flex for input to take available space 
                                                                'fontSize': '0.9em',  # Adjust font size to make textbox smaller
                                                                'resize': 'none',
                                                                'width': '25em',
                                                                'height': '10em'
                                                                }
                                                            )
                                                        ]),
                                                        dbc.ModalFooter(
                                                            dbc.Button(translation['save_changes'], 
                                                                    id="modal-save-btn", 
                                                                    className="ms-auto", 
                                                                    n_clicks=0))    
                                                            ],
                                                            id='node-edit-modal',
                                                            is_open=False,
                                                            style = {'zIndex':'2000',
                                                                     'fontFamily': "Outfit",
                                                                     "fontWeight": 300,
                                                                     'fontSize': '18px'}),

                                            # Modal for edge info
                                            dbc.Modal([
                                                dbc.ModalHeader(
                                                    dbc.ModalTitle(translation['connection_edit_title'])),
                                                    dbc.ModalBody([
                                                        html.Div(id='edge-explanation'),
                                                        html.Br(),
                                                        html.Div(translation['connection_edit_strength']),
                                                        dcc.Slider(id='edge-strength', 
                                                                min=1, 
                                                                max=5, 
                                                                step=1),
                                                        html.Br(),
                                                        html.Div(translation['connection_types']),
                                                        dcc.Dropdown(id='edge-type-dropdown', 
                                                                    options=[#{'label': 'Default', 'value': 'default'},
                                                                            {'label': translation['type_01'], 
                                                                            'value': 'amplifier'},
                                                                            {'label': translation['type_02'], 
                                                                            'value': 'reliever'}],
                                                                    placeholder='Select a custom color', 
                                                                    multi=False, 
                                                                    style={'width': '70%', 
                                                                            'borderRadius': '10px'}),
                                                        html.Br(),
                                                        html.Div(translation['note']),
                                                        dcc.Textarea(
                                                            id='edge-annotation',
                                                            value='',
                                                            className='custom-textarea',
                                                            style={
                                                                'flex': '1',  # Flex for input to take available space 
                                                                'fontSize': '0.9em',  # Adjust font size to make textbox smaller
                                                                'resize': 'none',
                                                                'width': '25em',
                                                                'height': '10em'
                                                                }
                                                            )
                                                        ]),
                                                        dbc.ModalFooter(
                                                            dbc.Button(translation['save_changes'], 
                                                                id="edge-save-btn", 
                                                                className="ms-auto", 
                                                                n_clicks=0))    
                                                            ],
                                                            id='edge-edit-modal',
                                                            is_open=False,
                                                            style = {'zIndex':'2000',
                                                            'fontFamily': "Outfit",
                                                                     "fontWeight": 300,
                                                                     'fontSize': '18px'}),

                                            # Modal for Donation info
                                            dbc.Modal([
                                                dbc.ModalHeader(
                                                    dbc.ModalTitle(translation['donation_title'])),
                                                    dbc.ModalBody(translation['donation_info'], 
                                                                id = 'donation-info'),
                                                    dbc.ModalFooter(
                                                        dbc.Button(translation['donation_button'], 
                                                                id="donation-agree", 
                                                                className="ms-auto", 
                                                                n_clicks=0))    
                                                            ],
                                                            id='donation-modal', 
                                                            is_open=False, 
                                                            style={'zIndex': '5000',
                                                            'fontFamily': "Outfit",
                                                                     "fontWeight": 300,
                                                                     'fontSize': '18px'}),

                                            ]
                                        ),
                            ],
                        ),
                    ],
                ),
            ],
        )


def create_tracking_tab(track_data, translation):
    return html.Div(
            style= {**COMMON_STYLE, 
               "background": "linear-gradient(to bottom, white, #f4f4f9, #d6ccff, #9b84ff, #6F4CFF)",
               #"marginLeft": "-12px"
               },
            children=[
                # Header with Welcome Message
                html.Div(
                    #style=HEADER_STYLE,
                    children=[
                        # Header with Welcome Message
                        html.Div(
                            #style=HEADER_STYLE,
                            children=[
                                html.H2(
                                    translation['compare-map-title_01'],
                                    style={"fontFamily": "Outfit", 
                                        #"fontWeight": "normal", 
                                        #"color": "black", 
                                        "fontSize": "36px",
                                        "color": "#4A4A8D",
                                        "fontWeight": 500,
                                        "textAlign": "center",
                                        "marginLeft": "-150px",
                                        "marginTop": "-95px"},
                                ),
                            ],
                        ),
                    ],
                ),

                html.Hr(style={"marginLeft": "0px", "width": "90%", "marginTop": "40px"}),

                # Navbar above the plot, overlapping with header
                dbc.Navbar(
                    dbc.Container([
                        dbc.Nav(
                            [
                                dbc.NavItem(
                                    dbc.NavLink(
                                        translation['plot_01'], 
                                        id="plot-current", 
                                        href="#", 
                                        active='exact',
                                        style={"padding": "3px 10px"}
                                    )
                                ),
                                dbc.NavItem(
                                    dbc.NavLink(
                                        translation['plot_02'], 
                                        id="plot-overall", 
                                        href="#", 
                                        active='exact',
                                        style={"padding": "3px 10px"}
                                    )
                                ),
                            ],
                            className="modes-plot", 
                            navbar=True, 
                            style={'width': '100%', 'justifyContent': 'space-between'}
                        ),
                    ]),
                    id= 'plot-switch',
                    color="light", 
                    className="mb-2", 
                    style={
                        'width': '22%', 
                        'position': 'fixed', 
                        'top': '250px',   # Adjusted to overlap with header height
                        'left': '14%',    # Adjust for horizontal centering
                        'borderRadius': '50px',
                        'zIndex': '2000',
                        'fontFamily': "Outfit",
                        "fontWeight": 300,
                        "fontSize": "18px"
                    }
                ),

                dbc.Tooltip(
                    translation['hover-plots'],
                    target="plot-switch",  # ID of the element to show the tooltip for
                    placement="top",
                    autohide=True,
                    delay={"show": 500, "hide": 100}
                ),
                
                # Main content container (text and video)
                html.Div(
                    style={**CONTENT_CONTAINER_STYLE},
                    children=[
                        # Plot section with question mark button
                        html.Div(
                            style={'position': 'relative', 'width': '500px', 'height': "61vh", 'padding': '10px', "backgroundColor": "rgba(255, 255, 255, 0.65)",
                                   'borderRadius': '15px', 'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)', 'zIndex': '0', "marginLeft": "13px", "marginTop": "35px"},
                            children=[
                                dcc.Store(id='data-ready', data=False),
                                html.Div([dcc.Graph(id='centrality-plot', 
                                                    style={
                                                        "backgroundColor": "transparent"
                                                        })], 
                                         id='graph-container',
                                         style={'width': '90%', 'height': '90%', 'borderRadius': '15px'}),
                                
                                # Question Mark Button
                                dbc.Button(
                                    [html.I(className="fas fa-solid fa-question")], 
                                    id='help-plot', 
                                    color="light", 
                                    className='delete-button',
                                    style={
                                        'border': '2px solid #6F4CFF', 
                                        'padding' : '3px 10px 3px 10px',
                                        'borderRadius': "50px",
                                        #'color': 'grey', 
                                        "backgroundColor": "transparent",
                                        "color": "#6F4CFF",
                                        "boxShadow": "0px 4px 8px rgba(0, 0, 0, 0.1)",
                                        'position': 'absolute', 'top': '15px', 'right': '15px', 'zIndex': '10'
                                    }
                                ),
                                dbc.Modal([
                                    dbc.ModalHeader(
                                        dbc.ModalTitle(translation['plot_modal_title'])),
                                        dbc.ModalBody("", id='modal-plot-body')], 
                                    id="modal-plot", is_open=False, backdrop=True, style={'fontFamily': "Outfit",
                                                                           "fontWeight": 300,
                                                                           'fontSize': '18px'}
                                ),
                            ]
                        ),

                        # Cytoscape graph section with vertically stacked controls
                        html.Div(
                            style={**VIDEO_CONTAINER_STYLE, 'flexDirection': 'column', 'alignItems': 'center', "marginRight": "90px", "marginTop": "40px", "backgroundColor": "transparent"},
                            children=[
                                cyto.Cytoscape(
                                    id='track-graph',
                                    elements=track_data.get('elements', []),
                                    layout={'name': 'cose', "padding": 10, "nodeRepulsion": 3500, "idealEdgeLength": 10, "edgeElasticity": 5000, "nestingFactor": 1.2,
                                            "gravity": 1, "numIter": 1000, "initialTemp": 200, "coolingFactor": 0.95, "minTemp": 1.0, 'fit': True},
                                    zoom=1,
                                    pan={'x': 200, 'y': 200},
                                    stylesheet=track_data['stylesheet'],
                                    style=VIDEO_STYLE
                                ),

                                # Slider and Uniform Style Toggle Below Graph
                                html.Div(
                                    style={'marginTop': '20px', 'width': '100%', 'textAlign': 'center', "backgroundColor": "transparent", "marginLeft": "-50px"},
                                    children=[
                                        dcc.Slider(id='timeline-slider',
                                            marks=track_data['timeline-marks'],
                                            min=track_data['timeline-min'],
                                            max=track_data['timeline-max'],
                                            value=track_data['timeline-value'],
                                            step=None,
                                            className='timeline-slider',
                                        ),
                                        html.Div(
                                            style={'display': 'flex', 'justifyContent': 'center', 'gap': '15px', 'marginTop': '25px'},
                                            children=[
                                                dbc.Checklist(
                                                    options=[{"label": "Uniform Style", "value": 0}],
                                                    value=[1],
                                                    id="uniform-switch",
                                                    switch=True,
                                                    style={'marginRight': "330px",
                                                           "fontFamily": "Outfit",
                                                           'whiteSpace': 'nowrap',
                                                           "width": "200px"}
                                                ),
                                                dcc.Upload(
                                                    id='upload-graph-tracking',
                                                    children=dbc.Button(
                                                        [html.I(className="fas fa-upload"), " ", "file"], 
                                                        className='delete-button',
                                                        style={
                                                            #'border': 'none', 
                                                               'color': 'white', 
                                                               #'backgroundColor': 'lightgray', 
                                                               'whiteSpace': 'nowrap',
                                                               'padding': '7px 10px 7px 10px',
                                                               "borderRadius": "50px",
                                                               "backgroundColor": "transparent",
                                                               "border": "2px solid white",
                                                               'fontFamily': "Outfit",
                                                               "boxShadow": "0px 4px 8px rgba(0, 0, 0, 0.1)",}
                                                    )
                                                ),
                                                # dbc.Button(
                                                #     html.I(className="fas fa-trash"), 
                                                #     id='delete-tracking-map', 
                                                #     color="danger", 
                                                #     style={'border': 'none', 
                                                #            'color': '#E57373', 
                                                #            'backgroundColor': 'lightgray', 
                                                #            'padding': '7px 15px 7px 15px',
                                                #            "borderRadius": "50px"}
                                                # ),

                                                dbc.Button(
                                                    html.I(className="fas fa-trash"), 
                                                    id='delete-tracking-map', 
                                                    style={
                                                        'border': 'none', 
                                                        'color': 'white',  # White icon color for consistency
                                                        'background': 'linear-gradient(to right, #FF6F61, #FF9C91)',  # Subtle gradient for the button
                                                        'padding': '10px 15px',  # Larger padding for better spacing
                                                        'borderRadius': '50px',  # Fully rounded corners
                                                        'boxShadow': '0px 4px 8px rgba(0, 0, 0, 0.1)',  # Subtle shadow for depth
                                                        'fontSize': '16px',  # Slightly larger icon size
                                                        'transition': 'transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out'  # Smooth hover effect
                                                    },
                                                    className='delete-button',  # Optional: add a class for easier styling later
                                                    n_clicks=0  # Optional: initialize with zero clicks
                                                )

                                            ]
                                        ),
                                        dbc.Tooltip(
                                            translation['hover-uniform'],
                                            target="uniform-switch",  # ID of the element to show the tooltip for
                                            placement="top",
                                            autohide=True,
                                            delay={"show": 500, "hide": 100}
                                        ),

                                        dbc.Tooltip(
                                            translation['hover-upload-tracking'],  # Tooltip text
                                            target='upload-graph-tracking',  # ID of the element to show the tooltip for
                                            placement="top",
                                            autohide=True, 
                                            delay={"show": 500, "hide": 100}
                                        ),

                                        dbc.Tooltip(
                                            translation['hover-delete-tracking'],  # Tooltip text
                                            target="delete-tracking-map",  # ID of the element to show the tooltip for
                                            placement="top",
                                            autohide=True, 
                                            delay={"show": 500, "hide": 100}  # Set delay for show and hide (milliseconds) # Adjust placement as needed (top, bottom, left, right)
                                        ),

                                    ]
                                )
                            ]
                        ),
                    ],
                ),
            ],
        )

# Function: Create demo page
def create_demo_page(translation):
    return html.Div(
        style={
            "textAlign": "center",
            "background": "linear-gradient(to bottom, white, #f4f4f9, #d6ccff, #9b84ff, #6F4CFF)",
            "fontFamily": "Outfit",
            "width": "100vw",
            "minHeight": "100vh",
            "display": "flex",
            "flexDirection": "column",
            "justifyContent": "center",
            "alignItems": "center",
            "overflowX": "hidden",
            "marginLeft": "-12px",
        },
        children=[
            # Header Section
            html.Div(
                children=[
                    html.Img(
                        src="/assets/new-logo.png",
                        style={"width": "200px", "marginBottom": "20px"},
                    ),
                    html.H1(
                        "Desktop Demo",
                        style={
                            "fontSize": "55px",
                            #"color": "#4A4A8D",
                            "color": "black",
                            "fontWeight": 500,
                            "fontFamily": "Outfit",
                        },
                    ),
                    html.P(
                        dcc.Markdown(translation['demo'], dangerously_allow_html=True),
                        style={"fontSize": "18px", "color": "#6c757d", "fontWeight": 300},
                    ),

                    html.Div(
                        children=[
                            dbc.Button(
                                translation['get-started'],
                                href="/psychoeducation",
                                #className="glowing-button",
                                className='delete-button',
                                style={
                                    "margin": "10px",
                                    "fontSize": "18px",
                                    "padding": "10px 20px",
                                    "backgroundColor": "#6F4CFF",
                                    "border": "none",
                                    "color": "white",
                                    "borderRadius": "50px",
                                    "boxShadow": "0px 4px 6px rgba(0, 0, 0, 0.2)"
                                },
                            ),
                            # dbc.Button(
                            #     translation['learn-more'],
                            #     className='delete-button',
                            #     href="/output",
                            #     style={
                            #         "margin": "10px",
                            #         "fontSize": "18px",
                            #         "padding": "10px 20px",
                            #         "backgroundColor": "transparent",
                            #         "color": "#6F4CFF",
                            #         "border": "2px solid #6F4CFF",
                            #         "borderRadius": "50px",
                            #         "boxShadow": "0px 4px 6px rgba(0, 0, 0, 0.2)"
                            #     },
                            # ),
                        ]
                    ),
                ],
                style={
                    "maxWidth": "900px",
                    "backgroundColor": "#fff",
                    "padding": "20px 40px",
                    "borderRadius": "30px",
                    "opacity": "0.9",
                    "boxShadow": "0px 4px 10px rgba(0, 0, 0, 0.1)",
                    "marginTop": "120px",
                },
            ),
            # Features Section
            html.Div(
                style={"marginTop": "50px", "width": "100%"},
                children=[
                    dbc.Row(
                        [
                            # Feature 1: Psychoeducation
                            dbc.Col(
                                html.A(
                                    href="/psychoeducation",  # Target URL
                                    style={"textDecoration": "none"},  # Remove underline
                                    children=html.Div(
                                        children=[
                                            html.Div(translation['step-1'], style={"width": "80px", "height": "40px", "borderRadius": "50px", "backgroundColor": "#6F4CFF", "color": "white", "display": "flex", "alignItems": "center", "justifyContent": "center", "fontSize": "18px", "margin": "auto", "font": "Outfit", "fontWeight": "500"}),
                                            #html.Span("①", style={"font": "Outfit","fontSize": "24px", "color": "#6F4CFF", "marginRight": "10px"}),
                                            html.H4(
                                                translation['psychoeducation'],
                                                style={
                                                    "marginTop": "10px",
                                                    "fontWeight": 600,
                                                    "color": "black",
                                                },
                                            ),
                                            html.P(
                                                translation['psychoeducation-sub'],
                                                style={
                                                    "fontSize": "17px",
                                                    "color": "black",
                                                    "fontWeight": 300,
                                                },
                                            ),
                                        ],
                                        style={
                                            #"backgroundColor": "#A5C9FF",
                                            "backgroundColor": "#C9E2FF",
                                            #"backgroundColor": "#D6E9F8",
                                            "borderRadius": "15px",
                                            "padding": "30px 20px",
                                            "textAlign": "center",
                                            "boxShadow": "0px 4px 10px rgba(0, 0, 0, 0.1)",
                                            "transition": "transform 0.2s ease-in-out",
                                        },
                                        className="feature-box",
                                    ),
                                ),
                                md=3,
                            ),
                            # Feature 2: Map Editor
                            dbc.Col(
                                html.A(
                                    href="/my-mental-health-map",  # Target URL
                                    style={"textDecoration": "none"},
                                    children=html.Div(
                                        children=[
                                            html.Div(translation['step-2'], style={"width": "80px", "height": "40px", "borderRadius": "50px", "backgroundColor": "#6F4CFF", "color": "white", "display": "flex", "alignItems": "center", "justifyContent": "center", "fontSize": "18px", "margin": "auto", "font": "Outfit", "fontWeight": "500"}),
                                            #html.Span("②", style={"fontSize": "24px", "color": "#6F4CFF", "marginRight": "10px"}),
                                            html.H4(
                                                translation['editor'],
                                                style={
                                                    "marginTop": "10px",
                                                    "fontWeight": 600,
                                                    "color": "black",
                                                },
                                            ),
                                            html.P(
                                                translation['editor-sub'],
                                                style={
                                                    "fontSize": "17px",
                                                    "color": "black",
                                                    "fontWeight": 300,
                                                },
                                            ),
                                        ],
                                        style={
                                            "backgroundColor": "#D6CCFF",
                                            "borderRadius": "15px",
                                            "padding": "30px 20px",
                                            "textAlign": "center",
                                            "boxShadow": "0px 4px 10px rgba(0, 0, 0, 0.1)",
                                            "transition": "transform 0.2s ease-in-out",
                                        },
                                        className="feature-box",
                                    ),
                                ),
                                md=3,
                            ),
                            # Feature 3: Map Tracker
                            dbc.Col(
                                html.A(
                                    href="/track-my-mental-health-map",  # Target URL
                                    style={"textDecoration": "none"},
                                    children=html.Div(
                                        children=[
                                            html.Div(translation['step-3'], style={"width": "80px", "height": "40px", "borderRadius": "50px", "backgroundColor": "#6F4CFF", "color": "white", "display": "flex", "alignItems": "center", "justifyContent": "center", "fontSize": "18px", "margin": "auto", "font": "Outfit", "fontWeight": "500"}),
                                            #html.Span("③", style={"fontSize": "24px", "color": "#6F4CFF", "marginRight": "10px"}),
                                            html.H4(
                                                translation['tracker'],
                                                style={
                                                    "marginTop": "10px",
                                                    "fontWeight": 600,
                                                    "color": "black",
                                                },
                                            ),
                                            html.P(
                                                translation['tracker-sub'],
                                                style={
                                                    "fontSize": "17px",
                                                    "color": "black",
                                                    "fontWeight": 300,
                                                },
                                            ),
                                        ],
                                        style={
                                            "backgroundColor": "#F4D9FF",
                                            "borderRadius": "15px",
                                            "padding": "30px 20px",
                                            "textAlign": "center",
                                            "boxShadow": "0px 4px 10px rgba(0, 0, 0, 0.1)",
                                            "transition": "transform 0.2s ease-in-out",
                                        },
                                        className="feature-box",
                                    ),
                                ),
                                md=3,
                            ),
                        ],
                        justify="center",
                        className="g-4",  # Adds spacing between columns
                    ),
                ],
            ),
        ],
    )

# Function: Create learn more page
def create_learn_more_page(translation):
    return html.Div(
        style={
            "minHeight": "100vh",
            "width": "100vw",
           "background": "linear-gradient(to bottom, white, #f4f4f9, #d6ccff, #9b84ff, #6F4CFF)",
            "fontFamily": "Outfit",
            "display": "flex",
            "flexDirection": "column",
            "alignItems": "center",
            "padding": "50px 20px",
            "color": "#333333",  # Dark text for readability
            "marginLeft": "-12px"
        },
        children=[
            # Page Title
            html.H1(
                #"PsySys - Psychological Systems Education",
                "About",
                style={
                    # "fontSize": "48px",
                    # "fontWeight": "500",
                    "color": "#4A4A8D",
                    #"marginBottom": "30px",
                    "marginTop": "105px",

                    "textAlign": "center",
                    "fontSize": "36px",
                    "color": "#4A4A8D",
                    #"color":"black",
                    "marginBottom": "20px",
                    "fontWeight": "500",
                    #"fontWeight": "bold"
                },
            ),
            # Content Container
            html.Div(
                style={
                    "maxWidth": "800px",
                    #"backgroundColor": "rgba(255, 255, 255, 0.8)",  # Semi-transparent white
                    "backgroundColor": "transparent",
                    "padding": "30px",
                    "borderRadius": "15px",
                    #"boxShadow": "0px 4px 10px rgba(0, 0, 0, 0.1)",
                    "textAlign": "left",
                },
                children=[
                    html.H4(translation["about-1-1"],
                            style={
                                "fontSize": "24px",  # Larger subtitle
                                "color": "#4A4A8D",
                                "fontWeight": "400",
                                "marginBottom": "15px",
                                "textAlign": "center"
                            },
                        ),
                        html.P(translation["about-1-2"],
                            style={
                                "fontSize": "20px",  # Larger subtitle
                                "color": "black",
                                "fontWeight": "300",
                                "marginBottom": "15px",
                            },
                        ),

                    # Text Content
                    html.H4(translation["about-2-1"],
                            style={
                                "fontSize": "24px",  # Larger subtitle
                                "color": "#4A4A8D",
                                "fontWeight": "400",
                                "marginBottom": "15px",
                                "textAlign": "center"
                            },
                        ),
                        html.P(translation["about-2-2"],
                            style={
                                "fontSize": "20px",  # Larger subtitle
                                "color": "black",
                                "fontWeight": "300",
                                "marginBottom": "25px",
                            },
                        ),

                        html.H4(translation["about-3-1"],
                            style={
                                "fontSize": "24px",  # Larger subtitle
                                "color": "#4A4A8D",
                                "fontWeight": "400",
                                "marginBottom": "15px",
                                "textAlign": "center"
                            },
                        ),
                        html.P(translation["about-3-2"],
                            style={
                                "fontSize": "20px",  # Larger subtitle
                                "color": "black",
                                "fontWeight": "300",
                                "marginBottom": "45px",
                            },
                        ),

                    # Images for Visual Appeal
                    # html.Img(
                    #     src="/assets/mental-health-illustration.png",
                    #     style={
                    #         "width": "100%",
                    #         "marginBottom": "20px",
                    #         "borderRadius": "10px",
                    #         "boxShadow": "0px 2px 6px rgba(0, 0, 0, 0.1)",
                    #     },
                    # ),
                    # Call-to-Action Buttons
                    html.Div(
                        style={"display": "flex", "gap": "20px", "justifyContent": "center"},
                        children=[
                            dbc.Button(
                                translation['get-started'],
                                href="/psysys-demo",
                                className='delete-button',
                                style={
                                    "backgroundColor": "#6F4CFF",
                                    "color": "white",
                                    "padding": "15px 30px",
                                    "borderRadius": "50px",
                                    "fontSize": "18px",
                                    "fontWeight": "500",
                                    "border": "none",
                                    "boxShadow": "0px 4px 6px rgba(0, 0, 0, 0.2)"
                                },
                            ),
                            dbc.Button(
                                translation['back-home'],
                                href="/",
                                className = 'delete-button',
                                style={
                                    "backgroundColor": "transparent",
                                    "color": "#white",
                                    "padding": "15px 30px",
                                    "borderRadius": "50px",
                                    "fontSize": "18px",
                                    "fontWeight": "500",
                                    "border": "2px solid white",
                                    "boxShadow": "0px 4px 6px rgba(0, 0, 0, 0.2)"
                                },
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )

def create_landing_page(translation):
    return html.Div(
        style={
            "height": "100vh",
            "width": "100vw",
            "background": "linear-gradient(to bottom, white, #f4f4f9, #d6ccff, #9b84ff, #6F4CFF)",
            "display": "flex",
            "alignItems": "center",
            "justifyContent": "center",
            "position": "relative",
            "fontFamily": "Outfit",
            "color": "white",
            "overflow": "hidden",
            "marginLeft": "-12px"
        },
        children=[
            # Top-left network image
            html.Div(
                style={
                    "position": "absolute",
                    "top": "5%",
                    "left": "0%",
                    "zIndex": "0",
                },
                children=[
                    html.Img(
                        src="/assets/network_2.png",
                        style={
                            "width": "500px",
                            "opacity": "0.5",
                            "transform": "rotate(15deg)",
                            "animation": "move-glow-1 4s infinite alternate",
                        },
                    ),
                ],
            ),
            # Bottom-left network image
            html.Div(
                style={
                    "position": "absolute",
                    "bottom": "0%",
                    "left": "-10%",
                    "zIndex": "0",
                },
                children=[
                    html.Img(
                        src="/assets/network_3.png",
                        style={
                            "width": "600px",
                            "opacity": "0.6",
                            "transform": "rotate(-10deg)",
                            "animation": "move-glow-2 6s infinite alternate",
                        },
                    ),
                ],
            ),
            # Bottom-right network image
            html.Div(
                style={
                    "position": "absolute",
                    "bottom": "-10%",
                    "right": "-5%",
                    "zIndex": "0",
                },
                children=[
                    html.Img(
                        src="/assets/network_4.png",
                        style={
                            "width": "900px",
                            "opacity": "0.4",
                            "transform": "rotate(10deg)",
                            "animation": "move-glow-3 3s infinite alternate",
                        },
                    ),
                ],
            ),
            # Top-right network image
            html.Div(
                style={
                    "position": "absolute",
                    "top": "0%",
                    "right": "0%",
                    "zIndex": "0",
                },
                children=[
                    html.Img(
                        src="/assets/network_2.png",
                        style={
                            "width": "600px",
                            "opacity": "0.3",
                            "transform": "rotate(-15deg)",
                        },
                    ),
                ],
            ),
            # Gradient Overlay to clear center
            html.Div(
                style={
                    "position": "absolute",
                    "top": "0",
                    "left": "0",
                    "width": "100%",
                    "height": "100%",
                    "background": "radial-gradient(circle, rgba(255,255,255,0.7) 10%, transparent 60%)",
                    "zIndex": "0",
                },
            ),
            # Main Content (Centered)
            html.Div(
                style={
                    "position": "relative",
                    "zIndex": "1",
                    "textAlign": "center",
                    "maxWidth": "800px",
                    "color": "white",
                    "margin": "0 auto",
                },
                children=[
                    html.H1(
                        translation['welcome-landing'],
                        style={
                            "fontSize": "60px",
                            "fontWeight": "bold",
                            #"fontWeight": 500,
                            "marginBottom": "20px",
                            "color": "#4A4A8D",
                        },
                    ),
                    html.P(
                        translation['sub-landing'],
                        style={
                            "fontSize": "23px",
                            "fontWeight": "300",
                            "lineHeight": "1.6",
                            "marginBottom": "30px",
                            "color": "#4A4A8D",
                        },
                    ),
                    # Call-to-Action Buttons
                    html.Div(
                        style={"display": "flex", "justifyContent": "center", "gap": "15px"},
                        children=[
                            dbc.Button(
                                translation['view-demo'],
                                className = 'delete-button',
                                href="/psysys-demo",
                                style={
                                    "backgroundColor": "#6F4CFF",
                                    "color": "white",
                                    "padding": "15px 30px",
                                    "borderRadius": "50px",
                                    "fontSize": "18px",
                                    "fontWeight": "500",
                                    "border": "none",
                                    "boxShadow": "0px 4px 6px rgba(0, 0, 0, 0.2)",
                                },
                            ),
                            # dbc.Button(
                            #     translation['learn-more'],
                            #     className = 'delete-button',
                            #     href="/project-info",
                            #     style={
                            #         "backgroundColor": "transparent",
                            #         "color": "#6F4CFF",
                            #         "padding": "15px 30px",
                            #         "borderRadius": "50px",
                            #         "fontSize": "18px",
                            #         "fontWeight": "500",
                            #         "border": "2px solid #6F4CFF",
                            #         "boxShadow": "0px 4px 6px rgba(0, 0, 0, 0.1)",
                            #     },
                            # ),
                        ],
                    ),
                ],
            ),
        ],
    )


def create_about(app, translation):
    return html.Div(
        style={
            "minHeight": "100vh",
            "width": "100vw",
            #"background": "linear-gradient(to right, white 190px, #f4f4f9 250px, #d6ccff 600px, #9b84ff 70%, #6F4CFF)",
            "background": "linear-gradient(to bottom, white, #f4f4f9, #d6ccff, #9b84ff, #6F4CFF)",
            "fontFamily": "Outfit",
            "padding": "50px 20px",
            "overflowX": "hidden",  # Prevent horizontal scrolling
            "marginLeft": "-12px"
        },
        children=[

            html.Div(style={"height": "105px"}),

            # Team Section
            html.Div(
                children=[
                    html.H3(
                        #"Our Team",
                        translation["team"],
                        #className="multi-color-text",
                        style={
                            "textAlign": "center",
                            "fontSize": "36px",
                            "color": "#4A4A8D",
                            #"color": "#6F4CFF",
                            "marginBottom": "30px",
                        },
                    ),
                    dbc.Row(
                        [
                            # Team Members
                            create_team_member(
                                app,
                                "Emily Campos Sindermann",
                                "DSC_5008.JPG",
                                #translation['freelance'],
                                translation['emily-role'],
                                translation['role_01'],
                                link="https://www.linkedin.com/in/emily-campos-sindermann-2575652a8/?original_referer=https%3A%2F%2Fwww%2Egoogle%2Ecom%2F&originalSubdomain=de",  # Example link
                            ),
                            create_team_member(
                                app,
                                "Denny Borsboom",
                                "profile_dennyborsboom.jpeg",
                                translation['denny-role'],
                                translation['role_02'],
                                link="https://dennyborsboom.com", 
                            ),
                            create_team_member(
                                app,
                                "Tessa Blanken",
                                "profile_tessablanken.jpeg",
                                translation['tessa-role'],  
                                translation['role_03'],
                                link="https://tfblanken.com/", 
                            ),
                            create_team_member(
                                app,
                                "Lars Klintwall",
                                "profile_larsklintwall.jpeg",
                                translation['lars-role'],
                                translation['role_04'],
                                 link="https://ki.se/en/people/lars-klintwall", 
                            ),
                        ],
                        justify="center",
                        style={"gap": "30px"},  # Uniform spacing between team members
                    ),
                ],
                style={"marginBottom": "50px"},
            ),
            # Collaborators Section
            html.Div(
                children=[
                    html.H3(
                        translation["collaborators"],
                        style={
                            "textAlign": "center",
                            "fontSize": "36px",
                            "color": "#4A4A8D",
                            "marginBottom": "30px",
                        },
                    ),
                    dbc.Row(
                        [
                            create_team_member(
                                app, 
                                "Julian Burger",
                                "profile_julianburger.jpeg", 
                                "Post-Doc @ Yale School of Public Health",
                                translation['role_04'],
                                link="https://ysph.yale.edu/profile/julian-burger/", ),
                            create_team_member(
                                app, 
                                "Mark Willems",
                                "mark_willems_2.jpeg", 
                                translation['mark-role'],
                                translation['role_04'],
                                link="https://www.birdthealth.nl/over-birdt/", ),
                            create_team_member(
                                app, 
                                "Felix Vogel",
                                "felix_vogel.jpeg", 
                                translation['felix-role'],
                                translation['role_04'],
                                link="https://www.researchgate.net/profile/Felix-Vogel-4", ),
                        ],
                        justify="center",
                        style={"gap": "30px"},  # Consistent spacing between collaborators
                    ),
                ],
                style={"marginBottom": "50px"},
            ),
        
            # Supporters Section
            html.Div(
                children=[
                    html.H3(
                        translation["supporters"],
                        style={
                            "textAlign": "center",
                            "fontSize": "36px",
                            "color": "#4A4A8D",
                            "marginBottom": "30px",
                        },
                    ),
                    dbc.Row(
                        [
                            create_supporter(app, 'uva-logo-3.png', translation['uva-support'], link="https://psyres.uva.nl/research-groups/grants/grants.html?cb"),
                            create_supporter(app, 'dptv-logo.png', translation["dptv-support"], link="https://www.dptv.de"),
                            create_supporter(app, 'zentrum-1.jpeg', translation['zu-support'], link="https://www.ueberleben.org"),
                        ],
                        justify="center",
                        style={"gap": "30px"},  # Consistent spacing between supporters
                    ),
                ],
                style={"marginBottom": "50px"},
            ),

            # Contact Us Section
            html.Div(
                style={
                    "textAlign": "center",
                    "marginTop": "50px",
                    "position": "relative",
                },
                children=[
                    dbc.Button(
                        translation['contact'],
                        className="button-hover-gradient",
                        #className='delete-button',
                        href="mailto:campos.sindermann@gmail.com?subject=Inquiry%20for%20PsySys%20App&",
                        style={
                            "backgroundColor": "transparent",
                            "color": "white",
                            "padding": "15px 30px",
                            "borderRadius": "50px",
                            "fontSize": "18px",
                            "fontWeight": "500",
                            "border": "2px solid white",
                            "boxShadow": "0px 4px 6px rgba(0, 0, 0, 0.2)"
                        },
                    ),
                ],
            ),
        ],
    )


# Helper Function for Team Member
# def create_team_member(app, name, img, institution, role):
#     return dbc.Col(
#         html.Div(
#             style={
#                 "textAlign": "center",
#                 "width": "200px",  # Fixed width ensures uniform spacing
#                 "margin": "0 auto",
#             },
#             children=[
#                 html.Img(
#                     src=app.get_asset_url(img),
#                     style={
#                         "width": "160px",  # Increased size
#                         "height": "160px",
#                         "borderRadius": "50%",  # Circle images
#                         "marginBottom": "10px",
#                     },
#                 ),
#                 html.P(
#                     name,
#                     style={"fontWeight": 500, "color": "#4A4A8D", "fontSize": "19px"},
#                 ),
#                 html.P(institution, style={"color": "#black", "fontSize": "16px", "fontWeight": 300}),
#                 # html.P(role, style={"color": "#6c757d", "fontSize": "14px"}),
#             ],
#         ),
#         width="auto",  # Dynamically adjust to fit content
#     )

def create_team_member(app, name, img, institution, role, link):
    return dbc.Col(
        html.A(  # Wrap the entire block with an anchor tag to make it clickable
            href=link,
            target="_blank",  # Open link in a new tab
            style={"textDecoration": "none"},  # Remove underline from the link
            children=html.Div(
                style={
                    "textAlign": "center",
                    "width": "200px",  # Fixed width ensures uniform spacing
                    "margin": "0 auto",
                    "transition": "transform 0.2s ease-in-out",  # Smooth transition for hover effect
                },
                children=[
                    html.Img(
                        src=app.get_asset_url(img),
                        style={
                            "width": "160px",  # Initial size
                            "height": "160px",
                            "borderRadius": "50%",  # Circle images
                            "marginBottom": "10px",
                            "transition": "transform 0.2s ease-in-out",  # Smooth scaling on hover
                        },
                        className="hover-enlarge",  # Optional class for additional styling
                    ),
                    html.P(
                        name,
                        style={"fontWeight": 500, "color": "#4A4A8D", "fontSize": "19px"},
                    ),
                    html.P(
                        institution,
                        style={
                            "color": "#000000",
                            "fontSize": "16px",
                            "fontWeight": 300,
                        },
                    ),
                ],
            ),
        ),
        width="auto",  # Dynamically adjust to fit content
    )


# Helper Function for Supporter with Logo and Text
# def create_supporter(app, img, description):
#     return dbc.Col(
#         html.Div(
#             style={
#                 "textAlign": "center",
#                 "width": "230px",  # Consistent width for each supporter
#                 "margin": "0 auto",
#             },
#             children=[
#                 html.Img(
#                     src=app.get_asset_url(img),
#                     style={
#                         "width": "200px",  # Adjust logo size
#                         #"height": "130px",  # Maintain aspect ratio
#                         "height": "120px",
#                         "borderRadius": "15px",  # Rounded edges
#                         "boxShadow": "0 2px 4px rgba(0, 0, 0, 0.1)",  # Optional shadow
#                         "marginBottom": "10px",
#                     },
#                 ),
#                 html.P(
#                     description,
#                     style={
#                         "fontSize": "16px",
#                         "fontWeight": 300,
#                         "color": "#black",  # Subtle gray text color
#                         "marginTop": "5px",
#                     },
#                 ),
#             ],
#         ),
#         width="auto",  # Dynamically adjust to fit content
#     )

def create_supporter(app, img, description, link):
    return dbc.Col(
        html.A(
            href=link,
            target="_blank",  # Open link in a new tab
            style={"textDecoration": "none"},
            children=html.Div(
                style={
                    "textAlign": "center",
                    "width": "230px",  # Consistent width for each supporter
                    "margin": "0 auto",
                    "transition": "transform 0.2s ease-in-out",
                },
                children=[
                    html.Img(
                        src=app.get_asset_url(img),
                        style={
                            "width": "200px",  # Adjust logo size
                            "height": "120px",  # Maintain aspect ratio
                            "borderRadius": "15px",  # Rounded edges
                            "boxShadow": "0 2px 4px rgba(0, 0, 0, 0.1)",  # Optional shadow
                            "marginBottom": "10px",
                            "transition": "transform 0.2s ease-in-out",
                        },
                        className="hover-enlarge",
                    ),
                    html.P(
                        description,
                        style={
                            "fontSize": "16px",
                            "fontWeight": 300,
                            "color": "#000000",  # Subtle gray text color
                            "marginTop": "5px",
                        },
                    ),
                ],
            ),
        ),
        width="auto",
    )



# Styles
SUPPORTER_LOGO_STYLE = {
    "width": "120px",  # Slightly larger for visual balance
    "height": "120px",
    "borderRadius": "50%",  # Circular logos
}

COLLABORATOR_STYLE = {
    "width": "140px",
    "height": "140px",
    "borderRadius": "50%",  # Circular collaborator images
}

import dash_bootstrap_components as dbc
from dash import html


def create_output_page(translation):
    # Helper function to create a single output box
    # def create_output_box(image, tag, title, action, action_link):
    #     return html.A(  # Make the entire box a clickable link
    #         href=action_link,  # The URL to redirect to
    #         style={
    #             "textDecoration": "none",  # Remove underline from link
    #             "color": "inherit",  # Inherit text color for hover consistency
    #         },
    #         children=html.Div(
    #             style={
    #                 "width": "400px",
    #                 "backgroundColor": "white",
    #                 "borderRadius": "15px",
    #                 "boxShadow": "0px 4px 10px rgba(0, 0, 0, 0.1)",
    #                 "overflow": "hidden",
    #                 "display": "flex",
    #                 "flexDirection": "column",
    #                 "transition": "transform 0.2s ease-in-out",  # Smooth hover animation
    #             },
    #             children=[
    #                 # Image Section
    #                 html.Div(
    #                     style={"position": "relative"},
    #                     children=[
    #                         html.Img(
    #                             src=image,
    #                             style={
    #                                 "width": "100%",
    #                                 "height": "200px",
    #                                 "objectFit": "cover",
    #                             },
    #                         ),
    #                         # Tag
    #                         html.Div(
    #                             tag,
    #                             style={
    #                                 "position": "absolute",
    #                                 "top": "10px",
    #                                 "right": "10px",
    #                                 "backgroundColor": "#6F4CFF",
    #                                 "color": "white",
    #                                 "padding": "5px 10px",
    #                                 "borderRadius": "20px",
    #                                 "fontSize": "12px",
    #                                 "fontWeight": "bold",
    #                             },
    #                         ),
    #                     ],
    #                 ),
    #                 # Content Section
    #                 html.Div(
    #                     style={
    #                         "padding": "30px",
    #                         "flex": "1",  # Ensure content takes up remaining space
    #                         "display": "flex",
    #                         "flexDirection": "column",
    #                         "justifyContent": "space-between",
    #                     },
    #                     children=[
    #                         # html.Br(),
    #                         html.Div(style={"height": "-20px"}),
    #                         # Title
    #                         html.H4(
    #                             title,
    #                             style={
    #                                 "marginBottom": "10px",
    #                                 "color": "black",
    #                                 "fontSize": "20px",
    #                                 "fontWeight": 500,
    #                             },
    #                         ),
    #                         # html.Br(),
    #                         html.Div(style={"height": "-20px"}),
    #                         # Action Link (kept for semantics but redundant since the box is clickable)
    #                         html.A(
    #                             action,
    #                             href=action_link,
    #                             style={
    #                                 "fontSize": "16px",
    #                                 "color": "#6F4CFF",
    #                                 "fontWeight": 300,
    #                                 "fontStyle": "italic",
    #                                 "textDecoration": "none",
    #                             },
    #                         ),
    #                     ],
    #                 ),
    #             ],
    #         ),
    #     )

    def create_output_box(image, tag, title, action, action_link, language_flag):
        return html.A(  # Make the entire box a clickable link
            href=action_link,  # The URL to redirect to
            style={
                "textDecoration": "none",  # Remove underline from link
                "color": "inherit",  # Inherit text color for hover consistency
            },
            children=html.Div(
                style={
                    "width": "400px",
                    "backgroundColor": "white",
                    "borderRadius": "15px",
                    "boxShadow": "0px 4px 10px rgba(0, 0, 0, 0.1)",
                    "overflow": "hidden",
                    "display": "flex",
                    "flexDirection": "column",
                    "transition": "transform 0.2s ease-in-out",  # Smooth hover animation
                },
                children=[
                    # Image Section
                    html.Div(
                        style={"position": "relative"},
                        children=[
                            html.Img(
                                src=image,
                                style={
                                    "width": "100%",
                                    "height": "200px",
                                    "objectFit": "cover",
                                },
                            ),
                            # Tag and Language Flag Section
                            html.Div(
                                style={
                                    "position": "absolute",
                                    "top": "10px",
                                    "right": "10px",
                                    "display": "flex",
                                    "alignItems": "center",
                                    "gap": "5px",  # Space between the tag and the flag
                                },
                                children=[
                                    # Tag
                                    html.Div(
                                        tag,
                                        style={
                                            "backgroundColor": "#6F4CFF",
                                            "color": "white",
                                            "padding": "5px 10px",
                                            "borderRadius": "20px",
                                            "fontSize": "12px",
                                            "fontWeight": "bold",
                                        },
                                    ),
                                    # Language Flag
                                    html.Img(
                                        src=language_flag,
                                        style={
                                            "width": "20px",  # Adjust the size of the flag
                                            "height": "20px",
                                            "borderRadius": "50%",  # Make the flag circular
                                        },
                                    ),
                                ],
                            ),
                        ],
                    ),
                    # Content Section
                    html.Div(
                        style={
                            "padding": "30px",
                            "flex": "1",  # Ensure content takes up remaining space
                            "display": "flex",
                            "flexDirection": "column",
                            "justifyContent": "space-between",
                        },
                        children=[
                            html.Div(style={"height": "-20px"}),  # Spacer
                            # Title
                            html.H4(
                                title,
                                style={
                                    "marginBottom": "10px",
                                    "color": "black",
                                    "fontSize": "20px",
                                    "fontWeight": 500,
                                },
                            ),
                            html.Div(style={"height": "-20px"}),  # Spacer
                            # Action Link (kept for semantics but redundant since the box is clickable)
                            html.A(
                                action,
                                href=action_link,
                                style={
                                    "fontSize": "16px",
                                    "color": "#6F4CFF",
                                    "fontWeight": 300,
                                    "fontStyle": "italic",
                                    "textDecoration": "none",
                                },
                            ),
                        ],
                    ),
                ],
            ),
        )

    # Main Page Layout
    return html.Div(
        style={
            "width": "100vw",
            "minHeight": "100vh",
            "background": "linear-gradient(to bottom, white, #f4f4f9, #d6ccff, #9b84ff, #6F4CFF)",
            "padding": "50px",
            "fontFamily": "Outfit",
            "marginLeft": "-12px"
        },
        children=[
            # Header Section
            # html.Div(style={"height": "150px"}),
            html.Div(style={"height": "100px"}),

            html.Div(
                "Output",
                style={
                    "textAlign": "center",
                    "fontSize": "36px",
                    "color": "#4A4A8D",
                    #"color":"black",
                    "marginBottom": "40px",
                    "fontWeight": "500",
                    #"fontWeight": "bold"
                },
            ),
            # html.Div(style={"height": "50px"}),
            # Outputs Section
            dbc.Container(
                [
                    # First Row
                    dbc.Row(
                        [
                            dbc.Col(
                                create_output_box(
                                    "/assets/master_thesis.jpg",
                                    "MASTER THESIS",
                                    "It's All About Perspective: Introducing PsySys as a Digital Network-Informed Psychoeducation for Depression",
                                    #"Master Thesis",
                                    translation['read-more'],
                                    "/thesis",
                                    "/assets/us.png",
                                ),
                                width=4,
                                className="feature-box",
                                style={"transition": "transform 0.2s ease-in-out"},
                            ),
                            dbc.Col(
                                create_output_box(
                                    "/assets/dptv_bild.jpg",
                                    "ARTICLE",
                                    #"Article",
                                    "PsySys: Wirksamkeit einer netzwerkbasierten Online-Psychoedukation bei Depression",
                                    translation['read-more'],
                                    "/article",
                                    "/assets/de.png",
                                ),
                                width=4,
                                className="feature-box",
                                style={"transition": "transform 0.2s ease-in-out"},
                            ),
                            dbc.Col(
                                create_output_box(
                                    "/assets/dptv-press.jpg",
                                    "PRESS",
                                    "Depressionen besser verstehen: Entwicklung eines Netzwerkansatzes",
                                    html.Div(translation['read-more'],style={"marginTop":"23px"}),
                                    "/press",
                                    "/assets/de.png",
                                ),
                                width=4,
                                className="feature-box",
                                style={"transition": "transform 0.2s ease-in-out"},
                            ),
                        ],
                        justify="center",
                        className="mb-4",
                    ),
                    # Second Row
                    dbc.Row(
                        [   dbc.Col(
                                create_output_box(
                                    "/assets/blog.jpg",
                                    "BLOG",
                                    "Changing Perspectives: Taking a New Approach to Understand Your Mental Health",
                                    translation['read-more'],
                                    "/blog",
                                    "/assets/us.png",
                                ),
                                width=4,
                                className="feature-box",
                                style={"transition": "transform 0.2s ease-in-out"},
                            ),
                            dbc.Col(
                                create_output_box(
                                    "/assets/system_thinking.jpg",
                                    "BLOG",
                                    "From Parts to Patterns: The Power of Systems Thinking",
                                    html.Div(translation['coming-soon'], style={"marginTop": "23px"}),
                                    "#",
                                    "/assets/us.png",
                                ),
                                width=4,
                            ),
                            dbc.Col(
                                create_output_box(
                                    "/assets/complex_systems.jpg",
                                    "BLOG",
                                    "Beyond Symptoms: Mental Health Through the Lens of Complexity",
                                    html.Div(translation['coming-soon'], style={"marginTop": "23px"}),
                                    "#",
                                    "/assets/us.png",
                                ),
                                width=4,
                            ),
                        ],
                        justify="center",
                    ),
                ]
            ),
        ],
    )


def create_blog_page(translation):
    # Main Blog Page Layout
    return html.Div(
        style={
            "width": "100%",
            "minHeight": "100vh",
            "background": "linear-gradient(to bottom, white, #f4f4f9, #d6ccff, #9b84ff, #6F4CFF)",
            "padding": "50px 20px",
            "fontFamily": "Outfit",
            "color": "#333333",
            "overflowX": "hidden",
            "marginLeft": "-0px"
        },
        children=[
            # Image at the Top with Rounded Edges
            html.Div(
                style={
                    "textAlign": "center",
                    "marginBottom": "30px",
                    "marginTop": "60px"
                },
                children=[
                    html.Img(
                        src="/assets/blog.jpg",  # Replace with your blog cover image path
                        style={
                            "width": "100%",
                            "maxWidth": "900px",
                            #"height": "auto",
                            "height": "400px",
                            "objectFit": "cover",
                            "borderRadius": "20px",  # Rounded edges
                            "boxShadow": "0px 6px 12px rgba(0, 0, 0, 0.15)",
                        },
                    )
                ],
            ),
            # Header Section
            html.Div(
                style={
                    "textAlign": "center",
                    "marginBottom": "50px",
                },
                children=[
                    html.H1(
                        "Changing Perspectives: Taking a New Approach to Understand Your Mental Health",
                        style={
                            "fontSize": "45px",
                            #"color": "#4A4A8D",
                            "color": "black",
                            "fontWeight": "600",
                            "marginBottom": "10px",
                            "textAlign": "left",  # Aligns text to the left
                            "maxWidth": "900px",  # Restrict width for better readability
                            "marginLeft": "250px",
                        },
                    ),
                    html.Div(
                        style={
                            "display": "flex",
                            "flexDirection": "column",
                            "alignItems": "flex-start",
                            "color": "grey",
                            "fontSize": "16px",
                            "fontWeight": "300",
                            "marginTop": "10px",
                            "marginBottom": "20px",
                            "maxWidth": "900px",
                            "marginLeft": "250px",  # Align to the left
                        },
                        children=[
                            html.Span(
                                "Blogpost for Center of Survival, Berlin · November 2024",
                                style={
                                    "marginBottom": "5px",
                                    "fontSize": "18px",
                                },
                            ),
                            html.Span(
                                "Author: Emily Campos Sindermann",
                                style={
                                    "fontSize": "18px",
                                    "fontStyle": "italic",
                                },
                            ),
                        ],
                    ),

                ],
            ),
            # Blog Sections
            html.Div(
                style={
                    #"backgroundColor": "rgba(255, 255, 255, 0.85)",  # Semi-transparent white
                    "backgroundColor": "transparent",
                    "borderRadius": "15px",  # Rounded corners
                    "padding": "35px",  # Inner spacing
                    "margin": "30px auto",  # Center the box with margins
                    "maxWidth": "900px",  # Restrict max width for readability
                    #"boxShadow": "0px 4px 10px rgba(0, 0, 0, 0.1)",  # Subtle shadow
                },
                children=[
                    html.Div(
                        children=[
                            html.H4(  # Subtitle 1
                                "Understanding the 'invisible': What defines a mental disorder?",
                                style={
                                    "fontSize": "20px",  # Larger subtitle
                                    "color": "black",
                                    "fontWeight": "600",
                                    "marginBottom": "15px",
                                },
                            ),
                            html.P(
                                "Struggling with your mental health can be quite overwhelming. It can sometimes feel as "
                                "though a gloomy fog has settled in your mind, obscuring your thoughts and emotions beyond "
                                "your control. You might not even know where this came from or what exactly you’re up "
                                "against. Unlike identifying a broken arm, grasping a psychological problem can be less obvious.",
                                style={
                                    "fontSize": "20px",  # Larger subtitle
                                    "color": "black",
                                    "fontWeight": "300",
                                    "marginBottom": "15px",
                                },
                            ),

                            html.H4(  # Subtitle 2
                                "Beyond One-Size-Fits-All: Rethinking Mental Health Diagnosis",
                                style={
                                    "fontSize": "20px",
                                    "color": "black",
                                    "fontWeight": "600",
                                    "marginBottom": "15px",
                                },
                            ),
                            html.P(
                                "Historically, the field of psychology has relied on the search for common causes to "
                                "understand, diagnose and treat mental disorders. Stemming from the medical sciences, this "
                                "view assumes that a set of observable symptoms a person is experiencing can be traced back "
                                "to an underlying cause, the disorder.",
                                style={
                                    "fontSize": "20px",  # Larger subtitle
                                    "color": "black",
                                    "fontWeight": "300",
                                    "marginBottom": "15px",
                                },
                            ),

                            html.H4(  # Subtitle 3
                                "Breaking the Silence: Addressing Stigma to Normalise Mental Health Conversations",
                                style={
                                    "fontSize": "20px",
                                    "color": "black",
                                    "fontWeight": "600",
                                    "marginBottom": "10px",
                                },
                            ),
                            html.P(
                                "Mapping and understanding symptoms is often crucial for receiving the right support. "
                                "However, fear of judgment or misunderstanding often complicates the diagnostic process, "
                                "creating further barriers to receiving proper care.",
                                style={
                                    "fontSize": "20px",  # Larger subtitle
                                    "color": "black",
                                    "fontWeight": "300",
                                    "marginBottom": "15px",
                                },
                            ),

                            html.H4(  # Subtitle 4
                                "Mapping Mental Health: A Personalised Approach Through the Network Lens",
                                style={
                                    "fontSize": "20px",
                                    "color": "black",
                                    "fontWeight": "600",
                                    "marginBottom": "10px",
                                },
                            ),
                            html.P(
                                "In recent years, the network perspective has gained considerable attention by shifting the "
                                "focus away from syndromes to symptoms. Here, we get rid of the notion of an underlying "
                                "causing disorder and zoom-in on the interplay between symptoms.",
                                style={
                                    "fontSize": "20px",  # Larger subtitle
                                    "color": "black",
                                    "fontWeight": "300",
                                    "marginBottom": "15px",
                                },
                            ),

                            html.H4(  # Subtitle 5
                                "Evolving Perspectives: Toward Personalised and Compassionate Mental Health Care",
                                style={
                                    "fontSize": "20px",
                                    "color": "black",
                                    "fontWeight": "600",
                                    "marginBottom": "10px",
                                },
                            ),
                            html.P(
                                "How we define, diagnose and treat mental disorders changes depending on how our "
                                "understanding evolves over time. As we continue to explore new perspectives on mental "
                                "health, the hope is to develop more effective, personalised treatments that address the specific "
                                "needs of each individual.",
                                style={
                                    "fontSize": "20px",  # Larger subtitle
                                    "color": "black",
                                    "fontWeight": "300",
                                    "marginBottom": "15px",
                                },
                            ),
                        ],
                        style={
                            "color": "#333333",  # Dark grey for body text
                            "fontSize": "18px",  # Normal text size
                            "lineHeight": "1.6",  # Spacing between lines
                            "textAlign": "left",
                        },
                    ),
                ]),

            # Back to Output Button
            html.Div(
                style={"textAlign": "center", "marginTop": "50px"},
                children=[
                    dbc.Button(
                        translation['back'],
                        className='delete-button',
                        href="/output",
                        style={
                            "backgroundColor": "#6F4CFF",
                            "color": "white",
                            "padding": "15px 30px",
                            "borderRadius": "50px",
                            "fontSize": "18px",
                            "fontWeight": "500",
                            "border": "none",
                            "boxShadow": "0px 4px 6px rgba(0, 0, 0, 0.2)"
                        },
                    ),
                ],
            ),
        ],
    )

def create_thesis_page(translation):
# Main Blog Page Layout
    return html.Div(
        style={
            "width": "100vw",
            "minHeight": "100vh",
            "background": "linear-gradient(to bottom, white, #f4f4f9, #d6ccff, #9b84ff, #6F4CFF)",
            "padding": "50px 20px",
            "fontFamily": "Outfit",
            "color": "#333333",
            "overflowX": "hidden",
            "marginLeft": "-12px"
        },
        children=[
            # Image at the Top with Rounded Edges
            html.Div(
                style={
                    "textAlign": "center",
                    "marginBottom": "30px",
                    "marginTop": "60px"
                },
                children=[
                    html.Img(
                        src="/assets/master_thesis.jpg",  # Replace with your blog cover image path
                        style={
                            "width": "100%",
                            "maxWidth": "900px",
                            #"height": "auto",
                            "height": "400px",
                            "objectFit": "cover",
                            "borderRadius": "20px",  # Rounded edges
                            "boxShadow": "0px 6px 12px rgba(0, 0, 0, 0.15)",
                        },
                    )
                ],
            ),
            # Header Section
            html.Div(
                style={
                    "textAlign": "center",
                    "marginBottom": "50px",
                },
                children=[
                    html.H1(
                        "It's All About Perspective: Introducing PsySys as a Digital Network-Informed Psychoeducation for Depression",
                        style={
                            "fontSize": "45px",
                            #"color": "#4A4A8D",
                            "color": "black",
                            "fontWeight": "600",
                            "marginBottom": "10px",
                            "textAlign": "left",  # Aligns text to the left
                            "maxWidth": "900px",  # Restrict width for better readability
                            "marginLeft": "250px",
                        },
                    ),
                    html.Div(
                        style={
                            "display": "flex",
                            "flexDirection": "column",
                            "alignItems": "flex-start",
                            "color": "grey",
                            "fontSize": "16px",
                            "fontWeight": "300",
                            "marginTop": "10px",
                            "marginBottom": "20px",
                            "maxWidth": "900px",
                            "marginLeft": "250px",  # Align to the left
                        },
                        children=[
                            html.Span(
                                "Psychology Research Master Thesis, University of Amsterdam · August 2023",
                                style={
                                    "marginBottom": "5px",
                                    "fontSize": "18px",
                                },
                            ),
                            html.Span(
                                "Author: Emily Campos Sindermann",
                                style={
                                    "fontSize": "18px",
                                    "fontStyle": "italic",
                                },
                            ),
                        ],
                    ),

                ],
            ),
            # Blog Sections
            html.Div(
                style={
                    #"backgroundColor": "rgba(255, 255, 255, 0.85)",  # Semi-transparent white
                    "backgroundColor": "transparent",
                    "borderRadius": "15px",  # Rounded corners
                    "padding": "35px",  # Inner spacing
                    "margin": "30px auto",  # Center the box with margins
                    "maxWidth": "900px",  # Restrict max width for readability
                    #"boxShadow": "0px 4px 10px rgba(0, 0, 0, 0.1)",  # Subtle shadow
                },
                children=[
                    html.Div(
                        children=[
                            html.H4(  # Subtitle 1
                                "Abstract",
                                style={
                                    "fontSize": "20px",  # Larger subtitle
                                    "color": "black",
                                    "fontWeight": "600",
                                    "marginBottom": "15px",
                                    "textAlign": "center"
                                    
                                },
                            ),
                            html.P(
                                "Major depressive disorder remains among the most prevalent mental disorders worldwide. Previous studies suggest that internal illness representations are critical to the trajectory and treatment effectiveness of depression. Thus, shifting individuals’ perspectives on their depressive complaints might be a promising strategy to enhance treatment outcome. The present study aims to do this by introducing PsySys, the first digital psychoeducation for depression rooted in the network approach of psychopathology. In a 20-30 minute session, PsySys is designed to convey the conceptual foundations of the network approach through explanatory videos and help participants internalize and apply them in practical exercises. After participating in a single PsySys session, participants showed less prognostic pessimism and an increase in perceived personal control, and understanding of their complaints. PsySys was generally well received and participants provided valuable insights to inform future work. Overall, our findings indicate that a brief network-informed psychoeducation may serve to improve people’s attitudes towards their depressive complaints, and thereby increase their motivation and susceptibility to treatment.",
                                style={
                                    "fontSize": "20px",  # Larger subtitle
                                    "color": "black",
                                    "fontWeight": "300",
                                    "marginBottom": "15px",
                                },
                            ),
                        ],
                        style={
                            "color": "#333333",  # Dark grey for body text
                            "fontSize": "18px",  # Normal text size
                            "lineHeight": "1.6",  # Spacing between lines
                            "textAlign": "left",
                        },
                    ),
                ]),

            # Back to Output Button
            html.Div(
                style={"textAlign": "center", "marginTop": "50px", "display": "flex", "justifyContent": "center", "gap": "20px"},
                children=[
                    # Back Button
                    dbc.Button(
                        translation['back'],
                        className='delete-button',
                        href="/output",
                        style={
                            "backgroundColor": "#6F4CFF",
                            "color": "white",
                            "padding": "15px 30px",
                            "borderRadius": "50px",
                            "fontSize": "18px",
                            "fontWeight": "500",
                            "border": "none",
                            "boxShadow": "0px 4px 6px rgba(0, 0, 0, 0.2)",
                        },
                    ),
                    # Download Button
                    html.A(
                        dbc.Button(
                            translation['read-more'],
                            className='delete-button',
                            style={
                                "backgroundColor": "transparent",
                                "color": "white",
                                "padding": "15px 30px",
                                "borderRadius": "50px",
                                "fontSize": "18px",
                                "fontWeight": "500",
                                "border": "2px solid white",  # Transparent button with white border
                                "boxShadow": "0px 4px 6px rgba(0, 0, 0, 0.2)",
                            },
                        ),
                        href="https://www.dptv.de/fileadmin/Redaktion/Bilder_und_Dokumente/Im_Fokus/Wissenschaft_und_Forschung/Masterarbeit_Emily_Campos_Sindermann.pdf",
                        download="Masterarbeit_Emily_Campos_Sindermann.pdf",  # Enables file download
                        target="_blank",  # Opens in a new tab
                        style={"textDecoration": "none"},  # Remove underline from link
                    ),
                ],
            )

        ],
    )

def create_article_page(translation):
# Main Blog Page Layout
    return html.Div(
        style={
            "width": "100vw",
            "minHeight": "100vh",
            "background": "linear-gradient(to bottom, white, #f4f4f9, #d6ccff, #9b84ff, #6F4CFF)",
            "padding": "50px 20px",
            "fontFamily": "Outfit",
            "color": "#333333",
            "overflowX": "hidden",
            "marginLeft": "-12px"
        },
        children=[
            # Image at the Top with Rounded Edges
            html.Div(
                style={
                    "textAlign": "center",
                    "marginBottom": "30px",
                    "marginTop": "60px"
                },
                children=[
                    html.Img(
                        src="/assets/dptv_bild.jpg",  # Replace with your blog cover image path
                        style={
                            "width": "100%",
                            "maxWidth": "900px",
                            #"height": "auto",
                            "height": "400px",
                            "objectFit": "cover",
                            "borderRadius": "20px",  # Rounded edges
                            "boxShadow": "0px 6px 12px rgba(0, 0, 0, 0.15)",
                        },
                    )
                ],
            ),
            # Header Section
            html.Div(
                style={
                    "textAlign": "center",
                    "marginBottom": "50px",
                },
                children=[
                    html.H1(
                        "PsySys: Wirksamkeit einer netzwerkbasierten Online-Psychoedukation bei Depression",
                        style={
                            "fontSize": "45px",
                            #"color": "#4A4A8D",
                            "color": "black",
                            "fontWeight": "600",
                            "marginBottom": "10px",
                            "textAlign": "left",  # Aligns text to the left
                            "maxWidth": "900px",  # Restrict width for better readability
                            "marginLeft": "250px",
                        },
                    ),
                    html.Div(
                        style={
                            "display": "flex",
                            "flexDirection": "column",
                            "alignItems": "flex-start",
                            "color": "grey",
                            "fontSize": "16px",
                            "fontWeight": "300",
                            "marginTop": "10px",
                            "marginBottom": "20px",
                            "maxWidth": "900px",
                            "marginLeft": "250px",  # Align to the left
                        },
                        children=[
                            html.Span(
                                "Fachartikel für das Magazin Psychotherapie Aktuell der Deutschen Psychotherapeuten Vereinigung · Juli 2024",
                                style={
                                    "marginBottom": "5px",
                                    "fontSize": "18px",
                                },
                            ),
                            html.Span(
                                "Autorin: Emily Campos Sindermann",
                                style={
                                    "fontSize": "18px",
                                    "fontStyle": "italic",
                                },
                            ),
                        ],
                    ),

                ],
            ),
            # Blog Sections
            html.Div(
                style={
                    #"backgroundColor": "rgba(255, 255, 255, 0.85)",  # Semi-transparent white
                    "backgroundColor": "transparent",
                    "borderRadius": "15px",  # Rounded corners
                    "padding": "35px",  # Inner spacing
                    "margin": "30px auto",  # Center the box with margins
                    "maxWidth": "900px",  # Restrict max width for readability
                    #"boxShadow": "0px 4px 10px rgba(0, 0, 0, 0.1)",  # Subtle shadow
                },
                children=[
                    html.Div(
                        children=[
                            html.H4(  # Subtitle 1
                                "Zusammenfassung",
                                style={
                                    "fontSize": "20px",  # Larger subtitle
                                    "color": "black",
                                    "fontWeight": "600",
                                    "marginBottom": "15px",
                                    "textAlign": "center"
                                    
                                },
                            ),
                            html.P(
                                "Depression zählt weltweit zu den häufigsten psychischen Erkrankungen. Studien zeigen, dass innere Krankheitsrepräsenta- tionen bei den Patient*innen den Verlauf und die Wirksamkeit der Behandlung beeinflussen. Eine verbesserte Perspektive der Betroffenen könnte demnach die Behandlungsergebnisse positiv beeinflussen. Diese Masterarbeit untersucht dies durch die Einführung von PsySys – der ersten digitalen Psychoedukation für Depressionen, die auf dem Netzwerkansatz der Psy- chopathologie basiert. In einer 30-minütigen Online-Sitzung vermittelt PsySys die Grundlagen des Netzwerkansatzes mittels Erklärungsvideos und Übungen. Nach nur einer Sitzung berichteten die Teilnehmer*innen von reduziertem prognostischem Pessimismus sowie einem gesteigerten Gefühl der Kontrolle und einem besseren Verständnis ihrer Beschwerden. Unsere Ergebnisse legen nahe, dass eine kurze netzwerkbasierte Psychoedukation die Einstellung der Betroffenen verbessern und dadurch ihre Motivation während der Behandlung steigern kann.",
                                style={
                                    "fontSize": "20px",  # Larger subtitle
                                    "color": "black",
                                    "fontWeight": "300",
                                    "marginBottom": "15px",
                                },
                            ),
                        ],
                        style={
                            "color": "#333333",  # Dark grey for body text
                            "fontSize": "18px",  # Normal text size
                            "lineHeight": "1.6",  # Spacing between lines
                            "textAlign": "left",
                        },
                    ),
                ]),

            # Back to Output Button
            html.Div(
                style={"textAlign": "center", "marginTop": "50px", "display": "flex", "justifyContent": "center", "gap": "20px"},
                children=[
                    # Back Button
                    dbc.Button(
                        translation['back'],
                        className='delete-button',
                        href="/output",
                        style={
                            "backgroundColor": "#6F4CFF",
                            "color": "white",
                            "padding": "15px 30px",
                            "borderRadius": "50px",
                            "fontSize": "18px",
                            "fontWeight": "500",
                            "border": "none",
                            "boxShadow": "0px 4px 6px rgba(0, 0, 0, 0.2)",
                        },
                    ),
                    # Download Button
                    html.A(
                        dbc.Button(
                            "Download",
                            className='delete-button',
                            style={
                                "backgroundColor": "transparent",
                                "color": "white",
                                "padding": "15px 30px",
                                "borderRadius": "50px",
                                "fontSize": "18px",
                                "fontWeight": "500",
                                "border": "2px solid white",  # Transparent button with white border
                                "boxShadow": "0px 4px 6px rgba(0, 0, 0, 0.2)",
                            },
                        ),
                        href="/assets/PsySys-article-dptv.pdf",
                        download="PsySys-article-dptv.pdf",  # Enables file download
                        target="_blank",  # Opens in a new tab
                        style={"textDecoration": "none"},  # Remove underline from link
                    ),
                ],
            )

        ],
    )

def create_press_page(translation):
# Main Blog Page Layout
    return html.Div(
        style={
            "width": "100vw",
            "minHeight": "100vh",
            "background": "linear-gradient(to bottom, white, #f4f4f9, #d6ccff, #9b84ff, #6F4CFF)",
            "padding": "50px 20px",
            "fontFamily": "Outfit",
            "color": "#333333",
            "overflowX": "hidden",
            "marginLeft": "-12px"
        },
        children=[
            # Image at the Top with Rounded Edges
            html.Div(
                style={
                    "textAlign": "center",
                    "marginBottom": "30px",
                    "marginTop": "60px"
                },
                children=[
                    html.Img(
                        src="/assets/dptv-press.jpg",  # Replace with your blog cover image path
                        style={
                            "width": "100%",
                            "maxWidth": "900px",
                            #"height": "auto",
                            "height": "400px",
                            "objectFit": "cover",
                            "borderRadius": "20px",  # Rounded edges
                            "boxShadow": "0px 6px 12px rgba(0, 0, 0, 0.15)",
                        },
                    )
                ],
            ),
            # Header Section
            html.Div(
                style={
                    "textAlign": "center",
                    "marginBottom": "50px",
                },
                children=[
                    html.H1(
                        "Depressionen besser verstehen: Entwicklung eines Netzwerkansatzes",
                        style={
                            "fontSize": "45px",
                            #"color": "#4A4A8D",
                            "color": "black",
                            "fontWeight": "600",
                            "marginBottom": "10px",
                            "textAlign": "left",  # Aligns text to the left
                            "maxWidth": "900px",  # Restrict width for better readability
                            "marginLeft": "250px",
                        },
                    ),
                    html.Div(
                        style={
                            "display": "flex",
                            "flexDirection": "column",
                            "alignItems": "flex-start",
                            "color": "grey",
                            "fontSize": "16px",
                            "fontWeight": "300",
                            "marginTop": "10px",
                            "marginBottom": "20px",
                            "maxWidth": "900px",
                            "marginLeft": "250px",  # Align to the left
                        },
                        children=[
                            html.Span(
                                "Pressemitteilung zum DPtV Masterforschungspreis 2024 · Juni 2024",
                                style={
                                    "marginBottom": "5px",
                                    "fontSize": "18px",
                                },
                            ),
                            html.Span(
                                "Pressesprecher: Hans Strömsdörfer",
                                style={
                                    "fontSize": "18px",
                                    "fontStyle": "italic",
                                },
                            ),
                        ],
                    ),

                ],
            ),
            # Blog Sections
            html.Div(
                style={
                    #"backgroundColor": "rgba(255, 255, 255, 0.85)",  # Semi-transparent white
                    "backgroundColor": "transparent",
                    "borderRadius": "15px",  # Rounded corners
                    "padding": "35px",  # Inner spacing
                    "margin": "30px auto",  # Center the box with margins
                    "maxWidth": "900px",  # Restrict max width for readability
                    "marginTop":"-30px",
                    #"boxShadow": "0px 4px 10px rgba(0, 0, 0, 0.1)",  # Subtle shadow
                },
                children=[
                    html.Div(
                        children=[
                            html.H4(  # Subtitle 1
                                "Emily Campos Sindermann gewinnt DPtV-Master-Forschungspreis 2024",
                                style={
                                    "fontSize": "20px",  # Larger subtitle
                                    "color": "black",
                                    "fontWeight": "600",
                                    "marginBottom": "15px",
                                    "textAlign": "center"
                                    
                                },
                            ),
                            html.P(
                                "Berlin, 5. Juni 2024 – „Emily Campos Sindermanns Masterarbeit ist eine besonders innovative Leistung mit versorgungsrelevantem Ergebnis. Ihre Online- Psychoedukation ,PsySys‘ hat das Potential, von hohem Nutzen für Depressions-Patient*innen und ein Add-on für die psychotherapeutische Versorgung zu sein“, lobt Barbara Lubisch, stellvertretende Bundesvorsitzende der Deutschen PsychotherapeutenVereinigung (DPtV) die Preisträgerin des Master-Forschungspreises 2024. Der Verband verlieh zum vierten Mal seinen mit 1.000 Euro dotierten Preis im Rahmen des DPtV-Symposiums. „PsySys“ basiert auf dem Ansatz, nach dem psychische Erkrankungen ein Netzwerk von miteinander interagierenden Symptomen darstellen.",
                                style={
                                    "fontSize": "20px",  # Larger subtitle
                                    "color": "black",
                                    "fontWeight": "300",
                                    "marginBottom": "15px",
                                },
                            ),
                        ],
                        style={
                            "color": "#333333",  # Dark grey for body text
                            "fontSize": "18px",  # Normal text size
                            "lineHeight": "1.6",  # Spacing between lines
                            "textAlign": "left",
                        },
                    ),
                ]),

            # Back to Output Button
            html.Div(
                style={"textAlign": "center", "marginTop": "50px", "display": "flex", "justifyContent": "center", "gap": "20px"},
                children=[
                    # Back Button
                    dbc.Button(
                        translation['back'],
                        href="/output",
                        className='delete-button',
                        style={
                            "backgroundColor": "#6F4CFF",
                            "color": "white",
                            "padding": "15px 30px",
                            "borderRadius": "50px",
                            "fontSize": "18px",
                            "fontWeight": "500",
                            "border": "none",
                            "boxShadow": "0px 4px 6px rgba(0, 0, 0, 0.2)",
                        },
                    ),
                    # Download Button
                    html.A(
                        dbc.Button(
                            translation['read-more'],
                            className='delete-button',
                            style={
                                "backgroundColor": "transparent",
                                "color": "white",
                                "padding": "15px 30px",
                                "borderRadius": "50px",
                                "fontSize": "18px",
                                "fontWeight": "500",
                                "border": "2px solid white",  # Transparent button with white border
                                "boxShadow": "0px 4px 6px rgba(0, 0, 0, 0.2)",
                            },
                        ),
                        href="https://www.dptv.de/fileadmin/Redaktion/Bilder_und_Dokumente/Aktuelles_News/Pressemitteilungen/2024/2024-06-05-Masterpreis_2024.pdf",
                        download="Pressemitteilung-preis.pdf",  # Enables file download
                        target="_blank",  # Opens in a new tab
                        style={"textDecoration": "none"},  # Remove underline from link
                    ),
                ],
            )

        ],
    )