import dash_bootstrap_components as dbc
from dash import dcc, html
from flask_app.dash_app.helper import graphs
import dash_leaflet as dl

# =====CARDS=====
# FOUND FELL DONUT
card_discovery = dbc.Card(
    dcc.Graph(
        id="donut_discovery",
        figure=graphs.donut_discovery
    )
)

# MASS HISTOGRAM
card_mass = dbc.Card([
    dcc.Graph(
        id="histogram_mass"
    ),
    dcc.Slider(
        id='mass_range',
        min=0,
        max=9,
        value=9,
        marks={
            0: '<0.01',
            1: '<1',
            2: '<10',
            3: '<100',
            4: '<1k',
            5: '<10k',
            6: '<100k',
            7: '<1M',
            8: '<10M',
            9: 'All'
        },
        updatemode='drag',
    )
])

# YEAR HISTOGRAM
card_year = dbc.Card(
    dcc.Graph(
        id="histogram_year",
        figure=graphs.histogram_year
    )
)

# TYPE DONUT
card_type_donut = dbc.Card(
    dcc.Graph(
        id="donut_type",
        figure=graphs.donut_type
    )
)

# GROUP TREE
card_group_tree = dbc.Card(
    dcc.Graph(
        id="tree_group",
        figure=graphs.tree_group
    )
)

# WORLD MAP
card_map = [
    dl.Map(
        id="scatter_world",
        style={"height": "500px"}
    ),
    html.P("Cumulative meteorite count per final year:"),
    dcc.Slider(
        id='filter_world',
        min=850,
        max=2050,
        step=100,
        value=2050,
        updatemode='drag',
        tooltip={"placement": "bottom", "always_visible": True}
    )]