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


# -- Data Processing --
# def grouping_vehicles(data_df):
#     vehicle_type = data_df['Vehicle Type']
#     detection_errors = 0
#     cars = 0
#     pedestrians = 0
#     uncertains = 0
#     for j in tqdm(range(len(vehicle_type))):
#         vehicle_type_sub = vehicle_type[636]
#         vehicle_type_sub = vehicle_type_sub.split('\\')
#         for i in range(len(vehicle_type)):
#             vehicle = vehicle_type_sub[i]
#             if vehicle == 'car':
#                 cars += 1
#             elif vehicle == 'detection error':
#                 detection_errors += 1
#             elif vehicle == 'pedestrian':
#                 pedestrians += 1
#             else:
#                 uncertains += 1
#     total_vehicles = [pedestrians, cars, uncertains, detection_errors]
#     return total_vehicles

# time_list = time_windowing(data_df, 'H', 1)
# data_df['Time Grouping'] = time_list
# date_list = time_windowing(data_df, 'D', 1)
# data_df['Date Grouping'] = date_list
#
# print(data_df)

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
        id='example-graph-2',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
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



    # Plot road usage per unit time
    dcc.Graph(
        figure=dict(
            data=[
                dict(
                    x=[1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003,
                       2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012],
                    y=[219, 146, 112, 127, 124, 180, 236, 207, 236, 263,
                       350, 430, 474, 526, 488, 537, 500, 439],
                    name='Rest of world',
                    marker=dict(
                        color='rgb(55, 83, 109)'
                    )
                ),
                dict(
                    x=[1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003,
                       2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012],
                    y=[16, 13, 10, 11, 28, 37, 43, 55, 56, 88, 105, 156, 270,
                       299, 340, 403, 549, 499],
                    name='China',
                    marker=dict(
                        color='rgb(26, 118, 255)'
                    )
                )
            ],
            layout=dict(
                title='US Export of Plastic Scrap',
                showlegend=True,
                legend=dict(
                    x=0,
                    y=1.0
                ),
                margin=dict(l=40, r=0, t=40, b=30)
            )
        ),
        style={'height': 300},
        id='my-graph'
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
    # html.H4(children='US Agriculture Exports (2011)', style={
    #     'textAlign': 'center',
    #     'color': colors['text']
    # }),
    # generate_table(df)


])

if __name__ == '__main__':
    app.run_server(debug=True)
