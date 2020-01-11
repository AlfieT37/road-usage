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


def generate_pie_charts(dataframe):
    label_list = dataframe['Type']
    values_list = dataframe['Percentage']

    labels = [[label_list[0], label_list[1], label_list[2]], [label_list[4], label_list[3]]]

    values = [[values_list[0], values_list[1], values_list[2]], [values_list[4], values_list[3]]]

    data = []
    x1 = 0
    x2 = 0.40
    for label, value in zip(labels, values):
        data.append(go.Pie(labels=label,
                           values=value,
                           hoverinfo='label+value+percent', textinfo='value',
                           domain={'x': [x1, x2], 'y': [0, 1]}
                           )
                    )
        x1 = x1 + 0.45
        x2 = x1 + 0.40
    return data


# -- Colours --
colors = {
    'background': '#FFFFFF',
    'text': '#7FDBFF'}

# ----------------------------------------------------------------------
# -- Assets --
# ----------------------------------------------------------------------
# -- Data for plots --
df = pd.read_csv('https://gist.githubusercontent.com/chriddyp/c78bf172206ce24f77d6363a2d754b59/raw/c353e8ef842413cae56ae3920b8fd78468aa4cb2/usa-agricultural-exports-2011.csv')
#data_df = pd.read_csv('Data_export2.csv')
week_df = pd.read_csv('data_week.csv')
time_df = pd.read_csv('data_time.csv')
totals_df = pd.read_csv('data_totals.csv')

# Weather data
weather_type_df = pd.read_csv('data_weather_type.csv')
temp_df = pd.read_csv('data_temp.csv')

# -- Run Functions --

totals_data = generate_pie_charts(totals_df)


# -- Data naming --
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

# Weather Type
Weather_type = weather_type_df['Type']
Total_weather = weather_type_df['Total']
Cars_weather = weather_type_df['Car']
Vans_weather = weather_type_df['Van']
Pedestrians_weather = weather_type_df['Pedestrian']

# Temperature
Temperature = temp_df['Temp']
Total_temp = temp_df['Total']
Cars_temp = temp_df['Car']
Vans_temp = temp_df['Van']
Pedestrians_temp = temp_df['Pedestrian']

# -- Text --
markdown_text = ''' 
## Introduction
This project is for internet of things.
This web app is powered coded in Dash: "A productive Python framework for building web applications".
'''
markdown_text2 = '''
# How to use
The app is easy to use, simply view either the experimental data or the meta analysis of the equipment.
'''

data_overview = ''' 
**Average Number of Vehicles detected per day** - 1500\n
**Total number of Vehicles** - 15,000\n
\n
**Most common weather** - Cloudy\n
**Average temperature** - 8 *degrees Centigrade*\n
\n
**
'''

weather_introduction_markdown = '''
This is weather
'''

totals_introduction_markdown = '''
This is total plots
'''

Pie_chart_introductions = '''
Intro to pie Charts
'''

# ---------------------------------------------------------------------
# Layout

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[

    # Titles
    html.H1(
        children='Road Usage',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    # Subtitles
    html.Div([
        html.Div(children='Sensing and Internet of Things Coursework', style={
            'textAlign': 'center',
            'color': colors['text']
        }),

        html.Div(children='by Alfie Thompson', style={
            'textAlign': 'center',
            'color': colors['text']
        }),
    ]),

    # Introduction
    html.Div([
        html.Div([
            dcc.Markdown(style={'columnCount': 1}, children=markdown_text)],
            style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Markdown(style={'columnCount': 1}, children=markdown_text2)],
            style={'width': '48%', 'display': 'inline-block'}),
    ]),


    # # -- Tabs -- (Controlling view-able data)
    # dcc.Tabs(
    #     id='tabs', value='1', children=[
    #         dcc.Tab(label='Experimental Data', value=1),
    #         dcc.Tab(label='Equipment Effectiveness', value=2)
    #     ]
    # ),
    # html.Div(id='tab-output'),
    #
    html.Div([
        html.H2(
            children='Data Overview', style={
                'textAlign': 'center'}),
        html.Div([
            dcc.Markdown(style={'columnCount': 2}, children=data_overview),
            # dcc.Markdown(style={'height': '300', 'width': '48%', 'display': 'inline-block'}, children=data_overview),
            # dcc.Markdown(style={'height': '300', 'width': '48%', 'display': 'inline-block'}, children=data_overview2),
            ])
    ]),
    # -- Weather Data --
    # Line Chart
    html.Div([
        # Section title and introductions
        html.H2(
            children='Weather Dependant', style={
                'textAlign': 'center'}),
        dcc.Markdown(style={'columnCount': 1}, children=weather_introduction_markdown),

        # Weather Module
        html.Div([
            # Bar Chart
            html.Div([
                dcc.Graph(
                    id='Weather Type plot',
                    figure={
                        'data': [
                            {'x': Weather_type, 'y': Cars_weather, 'type': 'bar', 'name': 'Cars'},
                            {'x': Weather_type, 'y': Pedestrians_weather, 'type': 'bar', 'name': u'Pedestrians'},
                            {'x': Weather_type, 'y': Vans_weather, 'type': 'bar', 'name': u'Vans'},

                        ],
                        'layout': {
                            'title': 'Average activity depending on Weather',
                            'plot_bgcolor': colors['background'],
                            'paper_bgcolor': colors['background'],
                            'xaxis': {'title': 'Time - Hours (24 hours)'},
                            'yaxis': {'title': 'Number of vehicles'}
                        }
                    }
                )
            ], style={'height': '300', 'width': '48%', 'display': 'inline-block'}),
            html.Div([
                dcc.Graph(
                    id='Temp plot',
                    figure={
                        'data': [
                            {'x': Temperature, 'y': Cars_temp, 'type': 'bar', 'name': 'Cars'},
                            {'x': Temperature, 'y': Pedestrians_temp, 'type': 'bar', 'name': u'Pedestrians'},
                            {'x': Temperature, 'y': Vans_temp, 'type': 'bar', 'name': u'Vans'},

                        ],
                        'layout': {
                            'title': 'Average activity depending on Temperature',
                            'plot_bgcolor': colors['background'],
                            'paper_bgcolor': colors['background'],
                            'xaxis': {'title': 'Time - Hours (24 hours)'},
                            'yaxis': {'title': 'Number of vehicles'}
                        }
                    }
                )
            ], style={'height': '300', 'width': '48%', 'display': 'inline-block'}),
        ]),

        # Line Graph
        html.Div([
            dcc.Graph(
                figure=dict(
                    data=[
                        dict(
                            x=Temperature,
                            y=Cars_temp,
                            name='Cars',
                            marker=dict(
                                color='rgb(55, 83, 109)'
                            )
                        ),
                        dict(
                            x=Temperature,
                            y=Pedestrians_temp,
                            name='Pedestrians',
                            marker=dict(
                                color='rgb(55, 83, 109)'
                            )
                        ),
                        dict(
                            x=Temperature,
                            y=Vans_temp,
                            name='Vans',
                            marker=dict(
                                color='rgb(55, 83, 109)'
                            )
                        )
                    ],
                    layout=dict(
                        title='Average activity depending on Temperature',
                        showlegend=True,
                        legend=dict(
                            x=0,
                            y=1.0
                        ),
                        margin=dict(l=40, r=0, t=40, b=30)
                    )
                ),
                style={'height': 300},
                id='temperature plot '
            )])
        ]),


    # -- Bar Chart plot --
    html.Div([

        html.H2(
            children='Total plotting', style={
                'textAlign': 'center'}),
        dcc.Markdown(style={'columnCount': 1}, children=totals_introduction_markdown),

        html.Div([
            # html.H3(
            #     children='Bar plots', style={
            #         'textAlign': 'center',
            #     }
            # ),
            html.Div([
                html.Div([
                    dcc.Graph(
                        id='Testing week plot',
                        figure={
                            'data': [
                                {'x': Day, 'y': Cars, 'type': 'bar', 'name': 'Cars'},
                                {'x': Day, 'y': Pedestrians, 'type': 'bar', 'name': u'Pedestrians'},
                                {'x': Day, 'y': Vans, 'type': 'bar', 'name': u'Vans'},

                            ],
                            'layout': {
                                'title': 'Average activity during Week - Measured per Day',
                                'plot_bgcolor': colors['background'],
                                'paper_bgcolor': colors['background'],
                                'xaxis': {'title': 'Day - 24 hour periods'},
                                'yaxis': {'title': 'Number of vehicles'}

                            }
                        }
                    )
                ], style={'width': '48%', 'display': 'inline-block'}),

                html.Div([
                    dcc.Graph(
                        id='Testing time plot',
                        figure={
                            'data': [
                                {'x': Time, 'y': Cars_hourly, 'type': 'bar', 'name': 'Cars'},
                                {'x': Time, 'y': Pedestrians_hourly, 'type': 'bar', 'name': u'Pedestrians'},
                                {'x': Time, 'y': Vans_hourly, 'type': 'bar', 'name': u'Vans'},

                            ],
                            'layout': {
                                'title': 'Average activity during Day - Measured per Hour',
                                'plot_bgcolor': colors['background'],
                                'paper_bgcolor': colors['background'],
                                'xaxis': {'title': 'Time - Hours (24 hours)'},
                                'yaxis': {'title': 'Number of vehicles'}
                            }
                        }
                    )
                ], style={'width': '48%', 'display': 'inline-block'}),
            ])
        ]),

        # Plot road usage per unit time ---------------------------
        # {'x': Day, 'y': Cars, 'type': 'bar', 'name': 'Cars'},
        # {'x': Day, 'y': Total, 'type': 'bar', 'name': u'Pedestrians'},
        # {'x': Day, 'y': Vans, 'type': 'bar', 'name': u'Vans'},
        html.Div([
            # html.H3(
            #     children='Graph plots', style={
            #         'textAlign': 'center',
            #     }
            # ),
            html.Div([
                dcc.Graph(
                    figure=dict(
                        data=[
                            dict(
                                x=Day,
                                y=Cars,
                                name='Cars',
                                marker=dict(
                                    color='rgb(55, 83, 109)'
                                )
                            ),
                            dict(
                                x=Day,
                                y=Pedestrians,
                                name='Pedestrians',
                                marker=dict(
                                    color='rgb(55, 83, 109)'
                                )
                            ),
                            dict(
                                x=Day,
                                y=Vans,
                                name='Vans',
                                marker=dict(
                                    color='rgb(55, 83, 109)'
                                )
                            )
                        ],
                        layout=dict(
                            title='Average activity during Week - Measured per Day',
                            xaxis_title='x axis',
                            yaxis_title='Y axis',
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
                )], style={'width': '48%', 'display': 'inline-block'}),

            # Time Plot
            html.Div([
                dcc.Graph(
                    figure=dict(
                        data=[
                            dict(
                                x=Time,
                                y=Cars_hourly,
                                name='Cars',
                                marker=dict(
                                    color='rgb(55, 83, 109)'
                                )
                            ),
                            dict(
                                x=Time,
                                y=Pedestrians_hourly,
                                name='Pedestrians',
                                marker=dict(
                                    color='rgb(55, 83, 109)'
                                )
                            ),
                            dict(
                                x=Time,
                                y=Vans_hourly,
                                name='Vans',
                                marker=dict(
                                    color='rgb(55, 83, 109)'
                                )
                            )
                        ],
                        layout=dict(
                            title='Average activity during day - Measured Per Hour',
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
                )], style={'width': '48%', 'display': 'inline-block'}),
            ]),
        ]),

    html.Div([
        html.H3(
            children='Pie Charts', style={
                'textAlign': 'center'}),
        dcc.Markdown(style={'columnCount': 1}, children=Pie_chart_introductions),
        # Pie Charts
        html.Div([dcc.Graph(figure={'data': totals_data})])
    ]),
])

if __name__ == '__main__':
    app.run_server(debug=True)
