__author__ = 'Andrew Ferruzza _ 111616974'

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# ------------------------------------------
# load in csv using pandas
data = pd.read_csv('top10s.csv', engine='python')
data_pie = pd.read_csv('top10s-withpiedata.csv', engine='python')
# extra data arrays
avg_energy_per_year = [77.90196078, 74.88679245, 75.48571429, 73.87323944, 67.77586207, 70.33684211, 67.2375,
                       69.16923077, 65.46875, 64.74193548]
years = ['2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019']

app = dash.Dash()

#Setup filtered scatter (slider)
slider_fig = px.scatter(data, y=data['POPULARITY'], animation_frame=data['YEAR'],
                        hover_data=['ARTIST', 'TITLE'], title='Popularity Songs Filtered By Year (Sorted By Index)',
                        color='POPULARITY', size='POPULARITY', log_y=True, marginal_x='rug')

#Energy in songs over time - code partially taken from Plotly website
energy_fig = go.Figure()
energy_fig.add_trace(go.Scatter(x=years, y=avg_energy_per_year, fillcolor='red'))
energy_fig.update_layout(title_text="Average Energy of Songs By Year (Aggregate Graph)")
energy_fig.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label="1y",
                     step="year",
                     stepmode="backward"),
                dict(count=5,
                     label="5y",
                     step="year",
                     stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
    )
)

# setup the Dash page
app.layout = html.Div([
    html.Div([
        # Simple Dash heading for the entire page
        html.H1(['Top Spotify Songs of the 2010s - CSE 332 Lab #5 - Andrew Ferruzza']),
        # Setup the bar graph, dropdown is only for the duration count
        html.Div([
            dcc.Dropdown(id='bar_dropdown', options=[
                {'label': 'Duration (in seconds) Count', 'value': 'DURATION'},
            ],
                         # Set Initial Value for the dropdown box and size, also dropdown box options
                         value='DURATION', clearable=False, multi=False, style={"width": "40%"},
                         )
        ]),
        # Next HTML layer is the bar graph itself
        html.Div([
            dcc.Graph('bar_graph')
        ]),
        html.Div([
            dcc.Dropdown(id='pie_dropdown', options=[
                {'label': 'Top Genres', 'value': 'GENRE-PIE'},
            ],
                         # Set Initial Value for the dropdown box and size, also dropdown box options
                         value='GENRE-PIE', clearable=False, multi=False, style={"width": "40%"},
                         )
        ]),
        # Next HTML layer is the bar graph itself
        html.Div([
            dcc.Graph('pie_graph')
        ]),
        # PC PLot
        html.Div([
            dcc.Graph(figure=slider_fig, style={'width': "100%", 'height': '500%'})
        ]),
        html.Div([
            dcc.Graph(figure=energy_fig, style={'width': "100%", 'height': '500%'})
        ]),
    ]),
])


# Bar Graph callback
@app.callback(
    Output(component_id='bar_graph', component_property='figure'),
    [
        Input(component_id='bar_dropdown', component_property='value')
    ]
)
# Display method -- sets up and displays the bar chart
def display_bar(bar_dropdown):
    df = data
    bar = px.histogram(data_frame=df, x=bar_dropdown, color_discrete_sequence=['OliveDrab'],
                       title='Histogram - Duration of Most Popular 2010s Spotify Songs (Y-Axis Log Scaled)',
                       log_y=True)
    return bar

@app.callback(
    Output(component_id='pie_graph', component_property='figure'),
    [
        Input(component_id='pie_dropdown', component_property='value')
    ]
)
# Display method -- sets up and displays the pie chart
def display_pie(pie_dropdown):
    dff = data_pie
    pie = px.pie(data_frame=dff, names=pie_dropdown, title='Pie Chart for The Top Genres',
                 color_discrete_sequence=px.colors.diverging.Portland, hole=0.2)
    return pie

if __name__ == '__main__':
    app.run_server(debug=True)
