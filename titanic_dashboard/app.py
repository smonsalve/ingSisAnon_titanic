import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
print(plotly.__version__)
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from dash.dependencies import Input, Output


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options


df = pd.read_csv("../Titanic/train.csv")

# df = pd.DataFrame({
#     "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
#     "Amount": [4, 1, 2, 2, 4, 5],
#     "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
# })

# fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

fig = go.Figure(data=[go.Pie(
                        labels=df.Pclass, 
                        values=df.Pclass.value_counts(),
                        title='Pasajeros según Clase')
                    ]
                )

ages_histogram = px.histogram(df, 
                   x="Age",
                   color="Sex"
                   )
                
                
@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return dcc.Graph(
                id='example-graph',
                figure=fig
            )
    elif tab == 'tab-2':
        return html.Div([
             dcc.Graph(
                id='ages_histogram',
                figure=ages_histogram
            )
        ])

app.layout = html.Div(children=[
    html.H1(children='Titanic Dashboard'),
    html.H2(children='by Sergio Monsalve'),

    html.Div(children='''
        Trying dash on Titanic Kaggle Data
    '''),

    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='Pie Chart', value='tab-1'),
        dcc.Tab(label='Tab two', value='tab-2'),
    ]),

    html.Div(id='tabs-content'),

])

if __name__ == '__main__':
    app.run_server(debug=True)





