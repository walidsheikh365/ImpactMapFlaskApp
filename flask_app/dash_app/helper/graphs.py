import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_csv("flask_app/dash_app/appdata/meteorite_data_with_countries.csv")

# =====GRAPHS======
# FOUND/FELL DONUT
donut_discovery = go.Figure(
    data=[go.Pie(
        labels=df["discovery"].unique(),
        values=df["discovery"].value_counts(),
        textposition="outside",
        insidetextorientation="radial",
        textinfo="label+value+percent",
        hole=0.5,
        pull=[0.2, 0],
    )]
)

donut_discovery.update_layout(
    title="Discovery donut",
)


# MASS HISTOGRAM
def create_mass(value):
    df_mass = df[df['mass'] <= (10 ** (value - 1))]

    histogram_mass = px.histogram(
        df_mass,
        x="mass",
        nbins=20,
        color="discovery",
        pattern_shape="type",
        log_y=True,
        marginal="box",
        title="Mass histogram",
    )

    histogram_mass.update_layout({
        "plot_bgcolor": "rgba(0, 0, 0, 0)",
        "paper_bgcolor": "rgba(0, 0, 0, 0)",
        "legend_traceorder": "reversed",
        "xaxis_title":  "mass (grams)"
    },
        bargap=0.2
    )

    return histogram_mass


# YEAR HISTOGRAM
histogram_year = px.histogram(
    df,
    x="year",
    color="discovery",
    pattern_shape="type",
    log_y=True,
    title="Year histogram"
)

histogram_year.update_layout({
    "plot_bgcolor": "rgba(0, 0, 0, 0)",
    "paper_bgcolor": "rgba(0, 0, 0, 0)",
    "legend_traceorder": "reversed"
    },
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(
                    label="Last Century",
                    step="year",
                    count=100,
                    stepmode="backward"
                ),
                dict(
                    label="Reset",
                    step="all"
                )
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
    )
)


# TYPE DONUT
donut_type = px.pie(
    df,
    values=df["type"].value_counts(),
    names=df["type"].unique(),
    hole=0.5,
    title="Type donut"
)

donut_type.update_layout({
    "plot_bgcolor": "rgba(0, 0, 0, 0)",
    "paper_bgcolor": "rgba(0, 0, 0, 0)"
})

donut_type.update_traces(
    textposition="outside",
    textinfo="percent+value+label"
)


# GROUP TREE
parents = ["" for i in range(len(df["group"].unique()))]

tree_group = px.treemap(
    df,
    values=df["group"].value_counts(),
    names=df["group"].unique(),
    parents=parents,
    title="Group treemap"
)

tree_group.update_layout({
    "plot_bgcolor": "rgba(0, 0, 0, 0)",
    "paper_bgcolor": "rgba(0, 0, 0, 0)"
})

tree_group.update_traces(
    textinfo="percent entry+value+label"
)
