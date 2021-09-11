import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc  # pip install dash-bootstrap-components
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import chart
import fxcmpy
import engineio
import socketio
import os

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])
chart_obj = chart.Chart("EURUSD", "H1")

app.layout = dbc.Container([
    chart_obj.create_chart_top_bar(),
    dbc.Row([
        dbc.Col([
            html.Div([
                dcc.Checklist(
                    id='toggle-rangeslider',
                    options=[{'label': 'Include Rangeslider',
                              'value': 'slider'}],
                    value=['slider']
                ),
                dcc.Graph(
                    id="graph",
                    config={"displayModeBar": False, "scrollZoom": True},
                ),
            ]),
        ], width=12),
    ], className='mb-12'),

], fluid=False)

@app.callback(
    Output("graph", "figure"),
    [Input("toggle-rangeslider", "value")])
def display_candlestick(value):
    fig = chart_obj.draw_chart()
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#fdfdfd')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#fdfdfd')
    fig.update_layout(
        xaxis_rangeslider_visible='slider' in value,
        margin_l=0,
        margin_r=0,
        margin_t=0,
        margin_b=0,
        plot_bgcolor="#F7F7F9",
        paper_bgcolor='#F7F7F9',
        dragmode="pan",
        yaxis={"mirror" : "allticks", 'side': 'right'}
    )
    return fig



if __name__ == '__main__':
    app.run_server(debug=False)