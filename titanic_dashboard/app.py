import dash
import plotly
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
df = pd.read_csv("../Titanic/train.csv")

figpie = go.Figure(
    data=[
        go.Pie(
            labels=df.Pclass,
            values=df.Pclass.value_counts(),
            title="Pasajeros según Clase",
        )
    ]
)

ages_histogram = px.histogram(df, x="Age", color="Sex", barmode="group")

tab1_layout = [html.Div([dcc.Graph(id="example-graph", figure=figpie)])]

tab2_layout = [html.Div([dcc.Graph(id="ages_histogram", figure=ages_histogram)])]

tab3_layout = [
    html.Div(
        [
            html.Div(
                [
                    dcc.RangeSlider(
                        id="my-range-slider",
                        min=0,
                        max=100,
                        step=1,
                        value=[0, 100],
                        marks={i: "{}".format(i) for i in range(0, 101, 5)},
                    ),
                    html.Div(id="output-container-range-slider"),
                ]
            ),
            html.Label("Clase:"),
            dcc.Dropdown(
                id="MM",
                options=[{"label": i, "value": i} for i in df.Pclass.unique()],
                value=[],
            ),
            dcc.Graph(id="graphtitanic", figure=ages_histogram),
            dcc.Graph(id="graphtitanicpie", figure=figpie),
        ]
    )
]

app.layout = html.Div(
    children=[
        html.H1(children="Titanic Dashboard"),
        html.H2(children="by Sergio Monsalve"),
        html.Div(
            children="""
        Trying dash on Titanic Kaggle Data
    """
        ),
        dcc.Tabs(
            id="tabs",
            value="tab-1",
            children=[
                dcc.Tab(label="Pie Chart", value="tab-1", children=tab1_layout),
                dcc.Tab(label="Tab two", value="tab-2", children=tab2_layout),
                dcc.Tab(label="Completo", value="tab-3", children=tab3_layout),
            ],
        ),
        html.Div(id="tabs-content"),
    ]
)


# Slider -> count graph
@app.callback(
    dash.dependencies.Output("output-container-range-slider", "children"),
    [dash.dependencies.Input("my-range-slider", "value")],
)
def update_output(value):
    # filtered_df = df[df.Age >=  && df.Age <= ]
    # print(value)
    return 'You have selected "{}"'.format(value)


@app.callback(
    Output(component_id="graphtitanic", component_property="figure"),
    [
        Input(component_id="MM", component_property="value"),
        Input(component_id="my-range-slider", component_property="value"),
    ],
)
def update_figure(selected_class, year_slider):
    print("selected_class")
    print(selected_class)
    if not selected_class:
        filtered_df = df
    else:
        filtered_df = df[df.Pclass == selected_class]

    print(selected_class)
    print(filtered_df)
    fitrado_edad = filtered_df[
        (filtered_df["Age"] >= int(year_slider[0]))
        & (filtered_df["Age"] <= int(year_slider[1]))
    ]
    # print(fitrado_edad)
    fig = px.histogram(fitrado_edad, x="Age", color="Sex", barmode="group")
    fig.update_layout(transition_duration=500)
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)

