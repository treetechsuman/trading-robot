import dash
from dash import dcc
from dash import html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import dash_bootstrap_components as dbc  # pip install dash-bootstrap-components
from dash.dependencies import Input, Output
import engineio
import socketio
import fxcmpy
import os
import datetime as dt


class Chart:
    def __init__(self, symbol: str, time_frame: str, style: str = "Bar"):
        self.symbol = symbol
        self.time_frame = time_frame
        self.style = style
        self.indicators = []

    def get_data(self):
        file_name = self.symbol + self.time_frame + ".csv"
        # check if data is already downloaded or nor
        # in future load data if it is lolder then two week
        if os.path.exists(file_name):
            df = pd.read_csv(file_name, parse_dates=True, index_col=0)
            return df
        else:
            TOKEN = "c4f7c3f82b7986f5d395c01c696e2c024b4d730e"
            con = fxcmpy.fxcmpy(access_token=TOKEN, log_level='error', server='demo', log_file='log.txt')
            start = dt.datetime(2017, 7, 15)
            stop = dt.datetime(2018, 8, 1)
            data = con.get_candles('EUR/USD', period=self.time_frame, start=start, stop=stop)
            df = pd.DataFrame(data)
            df.to_csv(file_name)
            return df

    def draw_chart(self):
        df = self.get_data()
        return go.Figure(go.Candlestick(
            x=df.index,
            open=df['askopen'],
            high=df['askhigh'],
            low=df['bidlow'],
            close=df['askclose']
        ))

    # layout of chart section
    def create_chart_top_bar(self):
        radioitems = dbc.FormGroup(
            [
                dbc.Label("Choose one"),
                dbc.RadioItems(
                    options=[
                        {"label": "Line", "value": 1},
                        {"label": "Candle", "value": 2},
                        {"label": "Bar", "value": 3},
                    ],
                    value=1,
                    id=self.symbol + "radioitems-input",
                ),
            ]
        )
        checklist = dbc.FormGroup(
            [
                dbc.Label("Choose Indicators"),
                dbc.Checklist(
                    options=[
                        {"label": "Moving Average", "value": 1},
                        {"label": "BB Band", "value": 2},
                        {"label": "ATR", "value": 3},
                    ],
                    value=[1],
                    id=self.symbol + "checklist-input",
                ),
            ]
        )
        tab1_content = dbc.Card(
            dbc.CardBody(
                [
                    radioitems,
                ]
            ),
            className="mt-3",
        )
        tab2_content = dbc.Card(
            dbc.CardBody(
                [
                    checklist,
                ]
            ),
            className="mt-3",
        )
        top_info = dbc.Row([
            dbc.Col([
                dbc.DropdownMenu(
                    label=self.symbol,
                    children=[
                        dbc.Tabs(
                            [
                                dbc.Tab(tab1_content, label="Style"),
                                dbc.Tab(tab2_content, label="Indicators"),
                            ]
                        ),
                    ], className="float-left col-4"
                ),

                dbc.Select(
                    id=self.symbol + "select",
                    options=[
                        {"label": "10 M", "value": "10M"},
                        {"label": "20 M", "value": "20M"},
                        {"label": "30 M", "value": "30M"},
                    ], value="10", className="float-right col-2",
                )

            ], width=12),
        ], className='mb-2 mt-2')
        return top_info
