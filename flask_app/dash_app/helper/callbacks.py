from dash.dependencies import Output, Input
from flask_app.dash_app.helper.graphs import *
from flask_app.dash_app.helper.world_map import world_map_by_year


def register_callbacks(dash_app):
    
    # When mass slider used, update histogram
    @dash_app.callback(
        Output("histogram_mass", "figure"),
        [Input("mass_range", "value")])
    def display_graph(value):
        histogram_mass = create_mass(value)

        return histogram_mass
    
    # When world scatter slider used, update map
    @dash_app.callback(
        Output("scatter_world", "children"),
        [Input("filter_world", "value")])
    def filter_world_map(year):
        scatter_world = world_map_by_year(year)

        return scatter_world
