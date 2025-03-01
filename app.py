import dash
import dash_bootstrap_components as dbc

app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        'https://use.fontawesome.com/releases/v6.6.0/css/all.css',
        'assets/styles.css'
    ],
    assets_folder='assets',
    suppress_callback_exceptions=True
)

app.title = "PsySys"

app.index_string = '''
<!DOCTYPE html>
<html>
<head>
    <script defer data-domain="https://psysys-study-uh.onrender.com" src="https://plausible.io/js/script.js"></script>
    {%metas%}
    <title>{%title%}</title>
    {%favicon%}
    {%css%}
</head>
<body>
    {%app_entry%}
    <footer>
        {%config%}
        {%scripts%}
        {%renderer%}
    </footer>
</body>
</html>
'''
