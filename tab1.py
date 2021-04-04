# -*- coding: utf-8 -*-
"""
Created on Sun Apr  4 18:08:29 2021

@author: MOHAMED
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd


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




tab1_layout = html.Div([

    html.H1('Exploring Genres in Movie Industry', style={ 'text-align': 'center','Color': '#228B22'}), #'background-color': '#000000',

    html.Div([
        html.Div([
            html.H1('Please choose 1 country', style={ 'text-align': 'center','fontColor': 'white'}), #'background-color': '#000000',
            dropdown_country,
            html.Br(),
            html.H1('Please choose 1 genre', style={'text-align': 'center','fontColor': 'white'}),#'background-color': '#000000', 
            dropdown_genre,
            html.Br(),
            radio_moviedata,
            year_slider
        ], style={'width': '20%', 'background-color': '#8B000000'}, className='box'),

        html.Div([
            html.Br(),
            html.Br(),
            dcc.Graph(id='graph_example'),
        ], style={'width': '80%', 'background-color': '#8B000000'}, className='box'),
            html.Br(),
            html.Br(),
            
        # html.Div(id="table1")#,style={'width': '80%'}, className='box')  
#        html.Div([
#            dcc.Graph(id='graph_example2')
#        ], style={'width': '80%'}, className='box')
    
    ], style={'display': 'flex','background-color': '#ADD8E6'}),


    html.Div([
        html.Br(),
        html.Br(),
        html.Div([
            dcc.Graph(id='graph_example2'),
        ], style={'width': '50%', 'background-color': '#8B000000'}, className='box'),

        html.Div([
            dcc.Graph(id='graph_example3'),
        ], style={'width': '50%', 'background-color': '#8B000000'}, className='box'),
        
#        html.Div([
#            dcc.Graph(id='graph_example2'),
#        ], style={'width': '33%', 'background-color': '#8B000000'}, className='box'),
    
    ], style={'display': 'flex'}),

])
