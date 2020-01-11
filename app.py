# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from PIL import Image
import plotly.graph_objects as go
from tqdm import tqdm

#from iot_functions import time_windowing

# ---------------------------------------------------------------------
# -- Initialisation --
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

# -- Data importing --
df = pd.read_csv('https://gist.githubusercontent.com/chriddyp/c78bf172206ce24f77d6363a2d754b59/raw/c353e8ef842413cae56ae3920b8fd78468aa4cb2/usa-agricultural-exports-2011.csv')
data_df = pd.read_csv('Data_export2.csv')
week_df = pd.read_csv('data_week.csv')
time_df = pd.read_csv('data_time.csv')

# -- Data naming
# Weekly data
Day = week_df['Day']
Total = week_df['Total']
Cars = week_df['Car']
Vans = week_df['Van']
Pedestrians = week_df['Pedestrian']

# Hourly Data
Time = time_df['Time']
Total_hourly = time_df['Total']
Cars_hourly = time_df['Car']
Vans_hourly = time_df['Van']
Pedestrians_hourly = time_df['Pedestrian']

# -- Generation of tables --
def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

def pie_chart(value):
    data = [
        {
            'values': [150, 300, 50][int(value)-1],
            'type': 'pie',
        }
    ]

# -- Colours --
colors = {
    'background': '#FFFFFF',
    'text': '#7FDBFF'
}

# ----------------------------------------------------------------------
# -- Assets --

# -- Data for plots --
#total_vehicles = grouping_vehicles(data_df)

# -- Text --
markdown_text = ''' 
## Introduction
This project is for internet of things.
This web app is powered coded in Dash: "A productive Python framework for building web applications".
# How to use
The app is easy to use, simply view either the experimental data or the meta analysis of the equipment.
# '''

data_overview = ''' 
## Data Overview 
**Average Number of Vehicles detected per day** - 1500\n
**Total number of Vehicles** - 15,000\n
\n
**Average weather** - Cloudy\n
**Average temperature** - 8 *degrees Centigrade*\n
\n
**
'''

# ---------------------------------------------------------------------
# Layout

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[

    # Titles
    html.H1(
        children='Hello Dash',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    # Subtitles
    html.Div(children='Dash: A web application framework for Python.', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    # Introduction
    dcc.Markdown(style={'columnCount': 2}, children=markdown_text),

    # -- Tabs -- (Controlling view-able data)
    dcc.Tabs(
        id='tabs', value='1', children=[
            dcc.Tab(label='Experimental Data', value=1),
            dcc.Tab(label='Equipment Effectiveness', value=2)
        ]
    ),
    html.Div(id='tab-output'),

    dcc.Markdown(style={'columnCount': 1}, children=data_overview),

    # -- Bar Chart plot --
    dcc.Graph(
        id='Testing week plot',
        figure={
            'data': [
                {'x': Day, 'y': Cars, 'type': 'bar', 'name': 'Cars'},
                {'x': Day, 'y': Pedestrians, 'type': 'bar', 'name': u'Pedestrians'},
                {'x': Day, 'y': Vans, 'type': 'bar', 'name': u'Vans'},

            ],
            'layout': {
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                }
            }
        }
    ),

    # Plot road usage per unit time ---------------------------
    # {'x': Day, 'y': Cars, 'type': 'bar', 'name': 'Cars'},
    # {'x': Day, 'y': Total, 'type': 'bar', 'name': u'Pedestrians'},
    # {'x': Day, 'y': Vans, 'type': 'bar', 'name': u'Vans'},
    dcc.Graph(
        figure=dict(
            data=[
                dict(
                    x=Day,
                    y=Total,
                    name='Total',
                    marker=dict(
                        color='rgb(55, 83, 109)'
                    )
                ),
                dict(
                    x=Day,
                    y=Cars,
                    name='Cars',
                    marker=dict(
                        color='rgb(26, 118, 255)'
                    )
                ),
                dict(
                    x=Day,
                    y=Pedestrians,
                    name='Pedestrians',
                    marker=dict(
                        color='rgb(26, 118, 255)'
                    )
                ),
                dict(
                    x=Day,
                    y=Vans,
                    name='Vans',
                    marker=dict(
                        color='rgb(26, 118, 255)'
                    )
                )
            ],
            layout=dict(
                title='Activity During day - Measured Per Hour',
                showlegend=True,
                legend=dict(
                    x=0,
                    y=1.0
                ),
                margin=dict(l=40, r=0, t=40, b=30)
            )
        ),
        style={'height': 300},
        id='my-graph1'
    ),
    dcc.Graph(
        figure=dict(
            data=[
                dict(
                    x=Time,
                    y=Total_hourly,
                    name='Total',
                    marker=dict(
                        color='rgb(55, 83, 109)'
                    )
                ),
                dict(
                    x=Time,
                    y=Cars_hourly,
                    name='Cars',
                    marker=dict(
                        color='rgb(26, 118, 255)'
                    )
                ),
                dict(
                    x=Time,
                    y=Pedestrians_hourly,
                    name='Pedestrians',
                    marker=dict(
                        color='rgb(26, 118, 255)'
                    )
                ),
                dict(
                    x=Time,
                    y=Vans_hourly,
                    name='Vans',
                    marker=dict(
                        color='rgb(26, 118, 255)'
                    )
                )
            ],
            layout=dict(
                title='Activity During day - Measured Per Hour',
                showlegend=True,
                legend=dict(
                    x=0,
                    y=1.0
                ),
                margin=dict(l=40, r=0, t=40, b=30)
            )
        ),
        style={'height': 300},
        id='my-graph2'
    ),






    dcc.Graph(
        id='graph',
        figure={
            'data': [go.Pie(labels=['Pedestrians', 'Cars', 'Undecided'], values=[150, 300, 50])],
            'layout': go.Layout(title=f'Road usage by vehicle', margin={'l': 300, 'r': 300},
                                legend={'x': 1, 'y': 0.7})
        }
    ),


    # # Table plot
    # html.H4(children='Vehicle Usage Per day', style={
    #     'textAlign': 'center',
    #     'color': colors['text']
    # }),
    # generate_table(date_df),
    #
    # generate_table(time_df)


])

if __name__ == '__main__':
    app.run_server(debug=True)
