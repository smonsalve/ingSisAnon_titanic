import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
df = pd.read_csv("../Titanic/train.csv")

figpie = go.Figure(data=[go.Pie(
                        labels=df.Pclass, 
                        values=df.Pclass.value_counts(),
                        title='Pasajeros según Clase')
                    ]
                )

ages_histogram = px.histogram(df, 
                   x="Age",
                   color="Sex",
                   barmode="group")


@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return dcc.Graph(
                id='example-graph',
                figure=figpie
            )
    elif tab == 'tab-2':
        return html.Div([
             dcc.Graph(
                id='ages_histogram',
                figure=ages_histogram
            )
        ])
    elif tab == 'tab-3':
        return html.Div([
            html.Label('Clase:'),
            dcc.Dropdown(
                id="MM",
                options=[
                    {
                            'label': i,
                            'value': i
                        } for i in df.Pclass.unique()
                ],
                value=[]
            ),
            dcc.Graph(
                id='graphtitanic',
                figure=ages_histogram
            ),
            dcc.Graph(
                id='graphtitanicpie',
                figure=figpie
            )
        ])

@app.callback(
    Output(component_id='graphtitanic', component_property='figure'),
    [Input(component_id='MM', component_property='value')]
)
def update_figure(selected_class):
    filtered_df = df[df.Pclass == selected_class]
    print(filtered_df)
    fig = px.histogram(filtered_df, x="Age", color="Sex", barmode="group")
    fig.update_layout(transition_duration=500)
    return fig



app.layout = html.Div(children=[
    html.H1(children='Titanic Dashboard'),
    html.H2(children='by Sergio Monsalve'),

    html.Div(children='''
        Trying dash on Titanic Kaggle Data
    '''),

    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='Pie Chart', value='tab-1'),
        dcc.Tab(label='Tab two', value='tab-2'),
        dcc.Tab(label='Completo', value='tab-3'),

    ]),

    html.Div(id='tabs-content'),

])

if __name__ == '__main__':
    app.run_server(debug=True)



