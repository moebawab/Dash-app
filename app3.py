# -*- coding: utf-8 -*-
"""
Created on Fri Apr  2 12:57:36 2021

@author: MOHAMED
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import plotly.graph_objs as go

# Dataset Processing

#path = 'https://raw.githubusercontent.com/nalpalhao/DV_Practival/master/datasets/'

#df = pd.read_csv(path + 'emissions.csv')

df = pd.read_csv('movies.csv',encoding='latin1')

"""
Equivalent way to iteratively build country_options from the dataset's countries:

country_options = [
    dict(label='Country ' + country, value=country)
    for country in df['country_name'].unique()]

 Try it out!
"""

country_options = [
    dict(label='Country ' + country, value=country)
    for country in df['country'].unique()]

genre_options = [
    dict(label='Genre ' + genre , value=genre)
    for genre in df['genre'].unique()]

moviedata_options = [
    {'label': 'Gross Revenue', 'value': 'gross'},
    {'label': 'Score', 'value': 'score'}
]

dropdown_country = dcc.Dropdown(
        id='country_drop',
        options=country_options,
        value=['USA'],
        multi=True
    )

dropdown_genre = dcc.Dropdown(
        id='genre_drop',
        options=genre_options,
        value=['Comedy'],
        multi=True
    )

radio_moviedata = dcc.RadioItems(
        id='moviedata_radio',
        options=moviedata_options,
        value='score',
        labelStyle={'display': 'block'}
    )

year_slider = dcc.RangeSlider(
        id='year_slider',
        min=1986,
        max=2016,
        value=[1986, 2016],
        marks={'1986': '1986',
               '1995': '1995',
               '2000': '2000',
               '2005': '2005',
               '2010': '2010',
               '2016': '2016'},
        step=1
    )

# The app itself

app = dash.Dash(__name__, external_stylesheets='')

app.layout = html.Div([

    html.H1('Exploring the different Genres in Movie Industry'),

    html.Div([
        html.Div([
            dropdown_country,
            html.Br(),
            dropdown_genre,
            html.Br(),
            radio_moviedata,
            year_slider
        ], style={'width': '20%', 'background-color': '#ffff00'}, className=''),

        html.Div([
            dcc.Graph(id='graph_example')
        ], style={'width': '80%'}, className='box')
    ], style={'display': 'flex'}),

#    html.Div([
#        year_slider
#    ], className='box')

])


@app.callback(
    Output('graph_example', 'figure'),
    [Input('country_drop', 'value'),
     Input('genre_drop', 'value'),
     Input('moviedata_radio', 'value'),
     Input('year_slider', 'value')]
)
def update_graph(countries,genres, moviedata, year):
    filtered_by_year_df = df[(df['year'] >= year[0]) & (df['year'] <= year[1])]

    scatter_data = []

    for country in countries:
        filtered_by_year_and_country_df = filtered_by_year_df.loc[filtered_by_year_df['country'] == country]
        
    for genre in genres:
        filtered_by_year_and_country_and_genre_df = filtered_by_year_and_country_df.loc[filtered_by_year_and_country_df['genre'] == genre]

        temp_data = dict(
            type='scatter',
            y=filtered_by_year_and_country_and_genre_df[moviedata],
            x=filtered_by_year_and_country_and_genre_df['year'],
            name=country+ genre
        )

        scatter_data.append(temp_data)

    scatter_layout = dict(xaxis=dict(title='Year'),
                          yaxis=dict(title=moviedata)
                          )

    fig = go.Figure(data=scatter_data, layout=scatter_layout)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
