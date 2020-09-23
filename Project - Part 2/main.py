__author__ = 'Andrew Ferruzza _ 111616974'

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

import plotly.express as px

import pandas as pd

# ------------------------------------------
# load in csv using pandas
# one csv is updated so the variable columns only display top 4 values + other for pie chart
data_pie = pd.read_csv('top10s-withpiedata.csv', engine='python')
data = pd.read_csv('top10s.csv', engine='python')

app = dash.Dash()

app.layout = html.Div([
    html.Div([
        # Simple Dash heading for the entire page
        html.H1(['Top Spotify Songs of the 2010s - CSE 332 Project #2 - Andrew Ferruzza']),
        # Create the dropdown menu for the pie graph
        dcc.Dropdown(id='pie_dropdown', options=[
            {'label': 'Title', 'value': 'TITLE-PIE'},
            {'label': 'Artist', 'value': 'ARTIST-PIE'},
            {'label': 'Genre', 'value': 'GENRE-PIE'},
            {'label': 'Year', 'value': 'YEAR-PIE'},
            {'label': 'BPM', 'value': 'BPM-PIE'},
            {'label': 'Energy', 'value': 'ENERGY-PIE'},
            {'label': 'dB', 'value': 'dB-PIE'},
            {'label': 'Duration (in seconds)', 'value': 'DURATION-PIE'},
            {'label': 'Speech', 'value': 'SPEECH-PIE'},
            {'label': 'Popularity', 'value': 'POPULARITY-PIE'}
        ],
                     # Set Initial Value for the dropdown box and size, also dropdown box options
                     value='TITLE-PIE', clearable=False, multi=False, style={"width": "40%"},
                     )
    ]),
    # Next HTML layer is the pie graph itself
    html.Div([
        dcc.Graph('pie_graph')
    ]),
    # Next Html layer is the bar graph dropdown
    html.Div([
        dcc.Dropdown(id='bar_dropdown', options=[
            {'label': 'Title Appearances', 'value': 'TITLE'},
            {'label': 'Artist and Song Count', 'value': 'ARTIST'},
            {'label': 'Genre and Song Count', 'value': 'GENRE'},
            {'label': 'Number of Songs per Year', 'value': 'YEAR'},
            {'label': 'BPM Count', 'value': 'BPM'},
            {'label': 'Energy Count', 'value': 'ENERGY'},
            {'label': 'dB Count', 'value': 'dB'},
            {'label': 'Duration (in seconds) Count', 'value': 'DURATION'},
            {'label': 'Speech Count', 'value': 'SPEECH'},
            {'label': 'Popularity Count', 'value': 'POPULARITY'}
        ],
                     # Set Initial Value for the dropdown box and size, also dropdown box options
                     value='TITLE', clearable=False, multi=False, style={"width": "40%"},
                     )
    ]),
    # Next HTML layer is the bar graph itself
    html.Div([
        dcc.Graph('bar_graph')
    ]),

    html.Div([
        html.H3('SELECT TWO OPTIONS TO CREATE A SCATTER PLOT:')
    ]),

    html.Div([
        html.H4('X-AXIS VALUE:')
    ]),
    # Dropdown box for scatter plot
    html.Div([
        dcc.Dropdown(id='scatter_dropdown1', options=[
            {'label': 'Title', 'value': 'TITLE'},
            {'label': 'Artist', 'value': 'ARTIST'},
            {'label': 'Genre', 'value': 'GENRE'},
            {'label': 'Year', 'value': 'YEAR'},
            {'label': 'BPM', 'value': 'BPM'},
            {'label': 'Energy', 'value': 'ENERGY'},
            {'label': 'dB (loudness)', 'value': 'dB'},
            {'label': 'Duration (in seconds)', 'value': 'DURATION'},
            {'label': 'Speech', 'value': 'SPEECH'},
            {'label': 'Popularity', 'value': 'POPULARITY'}
        ],
                     value='GENRE', clearable=False, multi=False, style={"width": "40%"},
                     )
    ]),

    html.Div([
        html.H4('Y-AXIS VALUE:')
    ]),

    html.Div([
        dcc.Dropdown(id='scatter_dropdown2', options=[
            {'label': 'Title', 'value': 'TITLE'},
            {'label': 'Artist', 'value': 'ARTIST'},
            {'label': 'Genre', 'value': 'GENRE'},
            {'label': 'Year', 'value': 'YEAR'},
            {'label': 'BPM', 'value': 'BPM'},
            {'label': 'Energy', 'value': 'ENERGY'},
            {'label': 'dB (loudness)', 'value': 'dB'},
            {'label': 'Duration (in seconds)', 'value': 'DURATION'},
            {'label': 'Speech', 'value': 'SPEECH'},
            {'label': 'Popularity', 'value': 'POPULARITY'}
        ],
                     value='YEAR', clearable=False, multi=False, style={"width": "40%"},
                     )
    ]),

    # Scatter plot graph
    html.Div([
        dcc.Graph('scatter')
    ])
])

# -----------------------------------------
# Callback section
# First callback for the pie chart
@app.callback(
    Output(component_id='pie_graph', component_property='figure'),
    [
        Input(component_id='pie_dropdown', component_property='value')
    ]
)
# Display method -- sets up and displays the pie chart
def display_pie(pie_dropdown):
    df = data_pie
    pie = px.pie(data_frame=df, names=pie_dropdown, title='Pie Chart for Top Spotify Songs of the 2010s')
    return pie


# Second callback is for the bar graph
@app.callback(
    Output(component_id='bar_graph', component_property='figure'),
    [
        Input(component_id='bar_dropdown', component_property='value')
    ]
)
# Display method -- sets up and displays the bar chart
def display_bar(bar_dropdown):
    dff = data
    bar = px.histogram(data_frame=dff, x=bar_dropdown, title='Bar Graph / Histogram for Top Spotify Songs of the 2010s')
    return bar


# Third and final callback for the scatter plot
@app.callback(
    Output(component_id='scatter', component_property='figure'),
    [
        Input(component_id='scatter_dropdown1', component_property='value'),
        Input(component_id='scatter_dropdown2', component_property='value')
    ]
)
# Display method -- sets up and displays scatter plot
def display_scatter(scatter_dropdown1, scatter_dropdown2):
    dfff = data
    scatter = px.scatter(data_frame=dfff, x=scatter_dropdown1, y=scatter_dropdown2, hover_data=['TITLE', 'ARTIST'],
                         title='Scatter Plot for Selected Variables', color=scatter_dropdown2, template='ggplot2')
    return scatter


if __name__ == '__main__':
    app.run_server(debug=True)
