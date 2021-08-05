import dash  # Dash 1.16 or higher
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table
import dash_bootstrap_components as dbc
import pathlib
import pandas as pd
import plotly.express as px
from app import app
# need to pip install statsmodels for trendline='ols' in scatter plot

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

# Data from U.S. Congress, Joint Economic Committee, Social Capital Project. https://www.jec.senate.gov/public/index.cfm/republicans/2018/4/the-geography-of-social-capital-in-america
df = pd.read_csv(r"C:\Users\User\Downloads\Perambur_Variance.csv")
data_table = dash_table.DataTable(
    id='data_table',
    columns=[{"name": i, "id": i} for i in df.columns],
    data=df.to_dict('records'),
)
data_store = dcc.Store(id = 'data-store',
                      data = df.to_dict('records'))
static_graph = dcc.Graph(
        id='bar-graph',
        figure={}
    )
layout = html.Div([
    dbc.Container(
    [
        dcc.Store(id="store"),
       html.H1('Perambur Assembly Constituency', style={"textAlign": "center"}),
    ]
     ),
    html.Label("Locations", style={'fontSize':30, 'textAlign':'center'}),
    dcc.Dropdown(
        id='states-dpdn',
        options=[{'label': s, 'value': s} for s in sorted(df.Location.unique())],
        value=None,
        clearable=False
    ),
    html.Label("Natures", style={'fontSize':30, 'textAlign':'center'}),
    dcc.Dropdown(id='counties2-dpdn',
                 options=[],
                 value=[],
                 multi=True),
    data_store,
    html.Br(),
    dcc.Loading([static_graph,
    data_table]),
    html.Br(),
])
# Populate the counties dropdown with options and values
@app.callback(
    Output('counties2-dpdn', 'options'),
    Output('counties2-dpdn', 'value'),
    Input('states-dpdn', 'value'),
)
def set_cities_options(chosen_state):
    dff = df[df.Location==chosen_state]
    counties2_of_states = [{'label': c, 'value': c} for c in sorted(dff.Nature.unique())]
    values_selected = [x['value'] for x in counties2_of_states]
    return counties2_of_states, values_selected


# Create graph component and populate with scatter plot
@app.callback([Output('data_table', 'data'),
    Output('bar-graph', 'figure')],
    [Input('counties2-dpdn', 'value'),
    Input('states-dpdn', 'value')],
    [State('data-store', 'data')]
)
def update_data_table(selected_counties2, selected_state, data_store):
    if len(selected_counties2) == 0:
        return dash.no_update
    else:
        df = pd.DataFrame(data_store)
        df = df[(df.Location==selected_state)]
        df = df[(df.Nature.isin(selected_counties2))]

    fig = px.bar(df, x='Nature', y='Votes', text='Votes', color = 'Parties', barmode="group")
    fig.update_traces(texttemplate='%{text:.2s}', textposition='inside')
    fig.update_layout(uniformtext_minsize=17, uniformtext_mode='hide')
    updated_data = df.to_dict('records')
    return updated_data, fig