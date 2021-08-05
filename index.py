import dash_core_components as dcc
import dash_html_components as html
from click import style
from dash.dependencies import Input, Output

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import summary, analytics



app.layout = html.Div([
html.Div([
                html.Img(src='/assets/my-image.png')
                  ],style={'textAlign': 'center'}),

    dcc.Location(id='url', refresh=False),

    html.Div([
        dcc.Link('Summary |', href='/apps/summary'),
        dcc.Link('Analytics ', href='/apps/analytics'),
    ], className="row"),
    html.Div(id='page-content', children=[])

])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/summary':
        return summary.layout
    if pathname == '/apps/analytics':
        return analytics.layout
    else:
        return "404 Page Error! Please choose a link"


if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)