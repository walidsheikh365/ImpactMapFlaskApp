import pandas as pd
import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash_extensions.javascript import Namespace

df = pd.read_csv("flask_app/dash_app/appdata/meteorite_data_with_countries.csv")

# WORLD MAP
def world_map_by_year(year):
    colorscale = ["green", "yellow", "red"]
    color_prop = "mass"

    # Setup data
    years_df = df[df['year'] <= year]
    map_df = years_df.dropna(subset=["latitude", "longitude"])
    dicts = map_df.to_dict(orient="records")

    # Setup element tooltip
    for meteorite in dicts:
        meteorite["tooltip"] = f'[{meteorite["name"]}]' \
                            f'[{meteorite["mass"]:.0f} grams]' \
                            f'[{meteorite["year"]:.0f}]' \
                            f'[{meteorite["country"]}'


    geojson = dlx.dicts_to_geojson(dicts, lat="latitude", lon="longitude")
    geobuf = dlx.geojson_to_geobuf(geojson)

    # Setup colormap & legend
    vmax = df[color_prop].max()
    colorbar = dl.Colorbar(
        colorscale=colorscale,
        width=20,
        height=150,
        min=0,
        max=vmax,
        unit="grams"
    )

    ns = Namespace("myNamespace", "mySubNamespace")

    # Setup elements on map
    geojson = dl.GeoJSON(
        data=geobuf,
        id="geojson",
        format="geobuf",
        cluster=True,
        zoomToBoundsOnClick=True,
        options=dict(pointToLayer=ns("pointToLayer")),
        superClusterOptions={"radius": 50},
        hideout=dict(
            colorProp=color_prop,
            circleOptions=dict(
                fillOpacity=1,
                stroke=False,
                radius=5),
            min=0,
            max=vmax,
            colorscale=colorscale
        )
    )

    # Create scatter
    scatter_world = dl.Map([
        dl.TileLayer(),
        geojson,
        colorbar,
    ], 
        id="scatter_world",
        style={"height": "500px"}
    )

    return scatter_world