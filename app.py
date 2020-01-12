# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
from PIL import Image
import plotly.graph_objects as go
from tqdm import tqdm
from datetime import datetime

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

    a=0
    for label, value in zip(labels, values):
        if a == 0:
            my_title = 'Proportion of total vehicles'
        else:
            my_title = 'Percentage of identified vehicles'
        data.append(go.Pie(labels=label,
                           values=value,
                           hoverinfo='label+value+percent', textinfo='value',
                           domain={'x': [x1, x2], 'y': [0, 1]},
                           title=my_title
                           )
                    )
        x1 = x1 + 0.45
        x2 = x1 + 0.40
        a += 1
    return data


def stacked_weather_chart(weather_type_list,cloud_weather,clear_weather,rain_weather):
    trace1 = go.Bar(
        x=weather_type_list, y=cloud_weather,
        name='Cloud'
    )
    trace2 = go.Bar(
        x=weather_type_list, y=clear_weather,
        name='Clear'
    )
    trace3 = go.Bar(
        x=weather_type_list, y=rain_weather,
        name='Rain'
    )
    data = [trace1, trace2, trace3]
    return data


# -- Colours --
colors = {
    'background': '#FFFFFF',
    'text': '#7FDBFF'}

# '#7FDBFF'

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
temp_df = pd.read_csv('data_temp.csv')
weather_type_df = pd.read_csv('data_weather_pct.csv')

# Uncertainty data
Uncertain_df = pd.read_csv('data_uncertain.csv')
Detection_df = pd.read_csv('data_detection.csv')

# -- Run Functions --

totals_data = generate_pie_charts(totals_df)  # Make Pie charts based off data


# -- Data naming --
# Weekly data
Day = week_df['Day']
Total = week_df['Total']
Cars = week_df['Car']
Vans = week_df['Van']
Pedestrians = week_df['Pedestrian']

# Hourly Data
Time = time_df['Hour']
Total_hourly = time_df['Total']
Cars_hourly = time_df['Car']
Uncertain_hourly = time_df['Uncertain']
Pedestrians_hourly = time_df['Pedestrian']

# Weather Type
Cloud_weather = weather_type_df['Cloud']
vehicle_type_weather = weather_type_df['Type']
Clear_weather = weather_type_df['Clear']
Rain_weather = weather_type_df['Rain']
Weather_type_list = ['Pedestrian', 'Car', 'Uncertain', 'Overall']
bar_data = stacked_weather_chart(Weather_type_list, Cloud_weather, Clear_weather, Rain_weather)

# Temperature
Temperature = temp_df['Temperature']
Total_temp = temp_df['Total']
Cars_temp = temp_df['Car']
Uncertain_temp = temp_df['Uncertain']
Pedestrians_temp = temp_df['Pedestrian']

# Uncertainty
Uncertain_time = Uncertain_df['Hour']
Uncertain_number = Uncertain_df['Number']
Detection_time = Detection_df['Hour']
Detection_number = Detection_df['Number']

# -- Text --
markdown_text = ''' 
## Introduction
This is a web app representing data from a Study into road usage in side streets in London, submitted for Sensing
and Internet of Things (SIoT) coursework.\n
All data is a available on the project's [Github Repository](https://github.com/AlfieT37/road-usage). This contains
processed data, source code and Remote Sensor module code. Photos are hosted privately to maintain data privacy. \n
##### Objectives
* Monitor and detect movement at street level
* Analyse data to identify the type of object detected
* Identify trends in road usage by **time**, **day** and **weather conditions**
* Present visualisation of data online - via a web app \n
##### Information about the study
This study spans over two weeks of data collection, with 16,600 samples. Future development of the study would
generate data that is useful for road planning and smart cities, who could redirect traffic based upon real data.\n
*For more information, contact me* - [Via email](mailto:alfiethompson37@gmail.com) *(alfiethompson37@gmail.com)*\n
##### Web app
This web app was coded in python using the in Dash: "A productive Python framework for building web applications". 
The web app is hosted for free via Heroku and, through it linkage to Github, is able to automatically rebuild when 
update data is generated. This would occur on a daily basis as the study continued. \n
*For more information:*
* Visit the Dash [documentation](https://dash.plot.ly/)
* Visit Heroku's [Website](https://www.heroku.com/)
* Visit Openweather's [Website](https://openweathermap.org/)

'''

data_overview = ''' 
**Average Number of Vehicles detected per day** - 709\n
**Total number of road uses** - 7804\n
\n
**Most common weather** - Cloudy\n
**Average temperature** - 299 kelvin\n
\n

'''

weather_introduction_markdown = '''
A key objective of the study was to understand how road usage is effected by weather effects. Below are two plots
that show the key trends found in the data.  
'''

totals_introduction_markdown = '''
Using the data gathered in this study, the trends of vehicle usage can be analysed.\n
This data is useful for understanding how the road is used **per hour** and **per day of the week**.\n
*The two plots can be viewed in either line or bar chart forms - __Simply click the tab to view__ *

'''

Pie_chart_introductions = '''
An important piece of information for this study is what proportion of correct detections are **Unidentified** or
**Vehicles**. \n
Of these, there is a distribution of total vehicles that have been correctly identified. 
'''

Meta_analysis = '''
The reliability of the Remote Sensor Module Can be evaluated here.\n
**"Uncertain" identifications** occur when the object detected from the image difference algorithm is larger than the
maximum size of the vehicles. These can occur when the object that has changed is not a real vehicle. A reduction
this number will come with better image analysis. \n
**Detection Errors** Occur when a large number of objects in the scene change. This can occur when light levels change,
when a few cars parked on the street change or any number of other reasons. When a large number of objects is detected,
the results should be marked as in valid.
'''

now = datetime.now()
last_updated_markdown = '''
*Last updated: %s*
''' %now

title_markdown = '''
**DE4 - Sensing and Internet of Things Coursework**\n
by Alfie Thompson
'''


# ---------------------------------------------------------------------
# Layout

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    # Titles
    html.Div([
        html.H1(
            children='- Road Usage Detection -',
            style={
                'textAlign': 'center',
                'color': 'white'
            }
        ),
        html.Div([
            dcc.Markdown(style={'columnCount': 1}, children=title_markdown),
        ], style={'textAlign': 'center', 'color': 'white'})

    ], style={'backgroundColor': '#053B41'}),

    dcc.Markdown(style={'columnCount': 1}, children=last_updated_markdown),

    # Introduction
    html.Div([
        html.Div([
            dcc.Markdown(style={'columnCount': 2}, children=markdown_text)])
    ]),

    html.H2(
        children='-- Road Usage Data --', style={
            'textAlign': 'Center'}),

    html.Div([
        html.H3(
            children='Data Overview', style={
                'textAlign': 'left'}),
        html.Div([
            dcc.Markdown(style={'columnCount': 2}, children=data_overview),
            ])
    ]),

    # -- Weather Data --
    # Line Chart
    html.Div([
        # Section title and introductions
        html.H3(
            children='Weather Dependent', style={
                'textAlign': 'left'}),
        dcc.Markdown(style={'columnCount': 1}, children=weather_introduction_markdown),

        # Weather Module
        html.Div([
            # Bar Chart
            html.Div([
                dcc.Graph(
                    figure=go.Figure(
                        data=bar_data,
                        layout=go.Layout(
                            title='Transport methods depending on weather',
                            barmode='stack',
                            xaxis=dict(tickvals=['Pedestrian', 'Car', 'Uncertain', 'Overall'], title='Vehicle type'),
                            yaxis=dict(title='Percentage of total detected vehicles'),
                            )
                          )
                )], style={'height': '300', 'width': '48%', 'display': 'inline-block'}),
                dcc.Graph(
                    figure=dict(
                        data=[
                            dict(
                                x=Temperature,
                                y=Total_temp,
                                name='Cars',
                                marker=dict(
                                    color='rgb(55, 83, 109)'
                                )
                            ),
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
                                y=Uncertain_temp,
                                name='Uncertainty',
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
                    style={'height': '300', 'width': '48%', 'display': 'inline-block'},
                    id='temperature plot '
            )])
    ]),

    # -- Bar Chart plot --
    html.Div([
        html.H3(
            children='Time Dependent', style={
                'textAlign': 'left'}),
        dcc.Markdown(style={'columnCount': 1}, children=totals_introduction_markdown),
        # -- Tabs -- (Controlling view-able data)
        dcc.Tabs(id="tabs-example", value='tab-1-example', children=[
            dcc.Tab(label='Line Chart Plotting', value='tab-1-example'),
            dcc.Tab(label='Bar Chart Plotting', value='tab-2-example'),
        ]),
        html.Div(id='tabs-content-example'),

        ]),

    # -- Pie Chart Plots --
    html.Div([
        html.Div([
            html.H3(
                children='Pie Charts', style={
                    'textAlign': 'left'}),
            dcc.Markdown(style={'columnCount': 1}, children=Pie_chart_introductions),
            ], style={'height': '200'}),
        # Pie Charts
        html.Div([
            html.Div([dcc.Graph(figure={'data': totals_data})])
        ], style={'height': '200'}),
    ]),

    # -- Uncertainty Plots --
    html.Div([
        html.H2(
            children='-- Study Meta Data --', style={
                'textAlign': 'left'}),
        dcc.Markdown(style={'columnCount': 1}, children=Meta_analysis),
        #
        html.Div([
            html.Div([
                dcc.Graph(
                    id='Uncertainty Plot',
                    figure={
                        'data': [
                            {'x': Uncertain_time, 'y': Uncertain_hourly, 'type': 'bar', 'name': 'Average'},

                        ],
                        'layout': {
                            'title': 'Average number of "Uncertain" identifications - per hour',
                            'plot_bgcolor': colors['background'],
                            'paper_bgcolor': colors['background'],
                            'xaxis': {'title': 'Time - Hours (24 hours)'},
                            'yaxis': {'title': 'Number of "Uncertain" identifications'}

                        }
                    }
                )
            ], style={'width': '48%', 'display': 'inline-block'}),

            html.Div([
                dcc.Graph(
                    id='Detection Error Plot',
                    figure={
                        'data': [
                            {'x': Detection_time, 'y': Detection_number, 'type': 'bar', 'name': 'Average'},

                        ],
                        'layout': {
                            'title': 'Average number of Detection errors - per hour',
                            'plot_bgcolor': colors['background'],
                            'paper_bgcolor': colors['background'],
                            'xaxis': {'title': 'Time - Hours (24 hours)'},
                            'yaxis': {'title': 'Number of Detection Errors'}
                        }
                    }
                )
            ], style={'width': '48%', 'display': 'inline-block'}),
        ])
    ]),
])


# ---------------------------------------------------------
# -- Callbacks --

@app.callback(Output('tabs-content-example', 'children'),
              [Input('tabs-example', 'value')])
def render_content(tab):
    if tab == 'tab-1-example':
        return html.Div([
            # html.H3('Line Charts'),
            html.Div([
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
                                    y=Uncertain_hourly,
                                    name='Uncertain',
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
        ])
    elif tab == 'tab-2-example':
        return html.Div([
            # html.H3('Bar Chart Plots'),
            html.Div([
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
                                    {'x': Time, 'y': Total_hourly, 'type': 'bar', 'name': 'Cars'},
                                    {'x': Time, 'y': Cars_hourly, 'type': 'bar', 'name': 'Cars'},
                                    {'x': Time, 'y': Pedestrians_hourly, 'type': 'bar', 'name': u'Pedestrians'},
                                    {'x': Time, 'y': Uncertain_hourly, 'type': 'bar', 'name': u'Uncertain'},

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
        ])


if __name__ == '__main__':
    app.run_server(debug=True)
