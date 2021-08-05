import plotly.express as px
import pandas as pd
import pathlib
import dash_bootstrap_components as dbc
import dash_table
import dash_html_components as html
import dash_core_components as dcc
from dash import dash
from dash.dependencies import Input, Output, State
from app import app

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

dfv = pd.read_csv(r"C:\Users\User\Downloads\Perambur_final.csv")
data_table = dash_table.DataTable(
    id='data-table',
    columns=[{"name": i, "id": i} for i in dfv.columns],
    data=dfv.to_dict('records'),
)
data_store = dcc.Store(id = 'data-store',
                      data = dfv.to_dict('records'))
static_graph = dcc.Graph(
        id='example-graph',
        figure={}
    )
layout = html.Div([
    dbc.Container(
    [
        dcc.Store(id="store"),
       html.H1('Perambur Assembly Constituency', style={"textAlign": "center"}),
dbc.Alert("Assembly constituency Number: 12",  style={"textAlign": "center"}, color="#FF5733"),
dbc.Alert("Assembly constituency Name: Perambur",  style={"textAlign": "center"}, color="#39FF33"),
    ]
     ),
    html.Label("Locations", style={'fontSize':30, 'textAlign':'center'}),
    dcc.Dropdown(
        id='states-dpdn',
        options=[{'label': s, 'value': s} for s in sorted(dfv.Location.unique())],
        value=None,
        clearable=False
    ),
    html.Label("Years", style={'fontSize':30, 'textAlign':'center'}),
    dcc.Dropdown(id='counties-dpdn',
                 options=[],
                 value=[],
                 multi=True),
    html.Label("Parties", style={'fontSize':30, 'textAlign':'center'}),
    dcc.Dropdown(
        id='party-dpdn',
        options=[{'label': s, 'value': s} for s in sorted(dfv.Parties.unique())],
        value=None,
        clearable=False
    ),
    data_store,
    html.Br(),
    dcc.Loading([static_graph,
    data_table]),
    html.Br(),
])
# Populate the counties dropdown with options and values
@app.callback(
    Output('counties-dpdn', 'options'),
    Output('counties-dpdn', 'value'),
    Input('states-dpdn', 'value'),
    Input('party-dpdn', 'value'),
)
def set_cities_options(chosen_state, chosen_party):
    dff = dfv[dfv.Location == chosen_state]
    dff = dfv[dfv.Parties == chosen_party]
    counties_of_states = [{'label': c, 'value': c} for c in sorted(dff.Years.unique())]
    values_selected = [x['value'] for x in counties_of_states]
    return counties_of_states, values_selected


# Create graph component and populate with scatter plot
@app.callback([Output('data-table', 'data'),
    Output('example-graph', 'figure')],
    [Input('counties-dpdn', 'value'),
    Input('states-dpdn', 'value'),
    Input('party-dpdn', 'value')],
    [State('data-store', 'data')]
)
def update_data_table(selected_counties, selected_state, selected_party, data_store):
    if len(selected_counties) == 0:
        return dash.no_update
    else:
        dfv = pd.DataFrame(data_store)
        dfv = dfv[(dfv.Location==selected_state)]
        dfv= dfv[(dfv.Years.isin(selected_counties))]
        dfv = dfv[(dfv.Parties == selected_party)]

    fig = px.bar(dfv, x='Years', y='Votes', text='Votes', color = 'Parties', barmode="group")
    fig.update_traces(texttemplate='%{text:.2s}', textposition='inside')
    fig.update_layout(uniformtext_minsize=17, uniformtext_mode='hide')
    updated_data = dfv.to_dict('records')
    return updated_data, fig
