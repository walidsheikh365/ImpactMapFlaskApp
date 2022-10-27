import dash
import dash_bootstrap_components as dbc
from flask_app.dash_app.helper.callbacks import register_callbacks
from flask_app.dash_app.helper.layout import layout

# RUN FROM TERMINAL WITH
# python -m flask_app.app

chroma = "https://cdnjs.cloudflare.com/ajax/libs/chroma-js/2.1.0/chroma.min.js"

external_stylesheets = [dbc.themes.LUX]

app = dash.Dash(
    __name__,
    external_scripts=[chroma],
    external_stylesheets=external_stylesheets,
    meta_tags=[{
        'content': 'width=device-width, initial-scale=1.0'
    }]
)

app.title = "Impact Map"
app.layout = layout
register_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True)
