from dash import html
import dash_bootstrap_components as dbc
from flask_app.dash_app.helper import cards, datatable
import base64

image_filename = "flask_app/dash_app/assets/logo.png"
PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"
encoded_image = base64.b64encode(open(image_filename, 'rb').read())


layout = html.Div(
    style={
        "margin-left": 10,
        "margin-right": 10,
        "margin-bottom": 10,
        "margin-top": 10,
        "text-align": "center"
    },

    children=[

        dbc.Navbar(
            dbc.Container([
                html.A(
                    # Use row and col to control vertical alignment of logo / brand
                    dbc.Row([
                        dbc.Col(html.Img(src=PLOTLY_LOGO, height="50px")),
                        dbc.Col(dbc.NavbarBrand("Meteorite Dashboard", className="ms-2")),
                    ],
                        align="center",
                        className="g-0",
                    ),
                    href="https://plotly.com",
                    style={"textDecoration": "none"},
                ),
                dbc.NavItem(dbc.NavLink("Back to Home page", href="/", external_link=True)),
            ]),
            color="light",
            dark=False,
            sticky='top',
            style={"height": "50px"},
        ),

        html.Br(),

        # Logo
        html.Div(
            html.Img(
                id="logo",
                src='data:image/png;base64,{}'.format(encoded_image.decode()),
                style={
                    "height": "20%",
                    "width": "20%"
                }
            )
        ),

        html.Br(),

        # Subtitle
        html.Div(
            id="subtitle",
            children="A Dash app created by Group 1 for COMP0034"
        ),

        html.Br(),

        # Cards
        dbc.Row([
            dbc.Col(cards.card_map, width=12)
        ],
            className="g-0"
        ),

        dbc.Row([
            dbc.Col(cards.card_mass, width=6),
            dbc.Col(cards.card_year, width=6)
        ],
            className="g-0",
            align="center",
        ),

        dbc.Row([
            dbc.Col(cards.card_discovery, width=4),
            dbc.Col(cards.card_type_donut, width=4),
            dbc.Col(cards.card_group_tree, width=4)
        ],
            className="g-0"
        ),

        html.Br(),

        dbc.Row([
            dbc.Col(datatable.datatable, width=12)
        ],
            className="g-0"
        )
    ]
)
