import pandas as pd
import dash_bootstrap_components as dbc
from dash import dash_table

df = pd.read_csv("flask_app/dash_app/appdata/meteorite_data_with_countries.csv")

# =====DATATABLE=====
datatable = dbc.Container(
    children=dash_table.DataTable(
        data=df.to_dict("records"),

        columns=[{"name": str(i), "id": str(i)} for i in df.columns],

        fixed_rows={
            "headers": True
        },

        style_table={
            "height": 400
        },

        style_cell={
            "font-size": 12,
            "border": "1px solid grey",
            "overflow": "hidden",
            "text-overflow": "ellipsis",
            "max-width": 0
        },

        style_data={
            "text-align": "right"
        },

        style_as_list_view=True,

        style_header={
            "font-weight": "bold"
        },

        tooltip_data=[
            {
                column: {"value": str(value), "type": "markdown"}
                for column, value in row.items()
            } for row in df.to_dict("records")
        ],

        tooltip_duration=None,

        filter_action="native",

        sort_action="native",

        sort_mode="multi",

        page_action="native",

        page_current=0,

        page_size=10
    )
)
