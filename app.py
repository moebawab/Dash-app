import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

################################# THE APP #################################

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, suppress_callback_exceptions=True,
                external_stylesheets = external_stylesheets)

app.title = "Movie Industry"

server = app.server

################################# FISRT TAB #################################

df = pd.read_csv('movies.csv',encoding='ISO-8859-1')

df.columns = df.columns.str.capitalize()

tab_1_layout = html.Div([
    html.Div([
        html.Div([
            html.Br(),
            html.Label(['Choose Country and Company:'],style={'font-weight': 'bold','font-size': '22px',
                                                              "text-align": "left",'color': '#ffffff'}),
            dcc.Dropdown(id = 'country_drop',
                options = [{'label':country, 'value':country} for country in df['Country'].unique()],
                value = 'USA',
                multi = False,
                disabled=False,
                clearable=True,
                searchable=True,
                placeholder='Choose Country...',
                className='form-dropdown',
                style={'width':"90%"},
                persistence='string',
                persistence_type='memory'),
        
            dcc.Dropdown(id = 'company_drop',
                options = [{'label':company, 'value':company} for company in df['Company'].unique()],
                value = 'Paramount Pictures',
                multi = False,
                disabled=False,
                clearable=True,
                searchable=True,
                placeholder='Choose Company..',
                className='form-dropdown',
                style={'width':"90%"},
                persistence='string',
                persistence_type='memory'),
            
            dcc.Dropdown(id= 'genre_drop',
            options = [{'label': genre, 'value' : genre} for genre in df['Genre'].unique()],
            value = 'Drama',
            multi = False,
            disabled=False,
            clearable=True,
            searchable=True,
            placeholder='Choose Genre..',
            className='form-dropdown',
            style={'width':"90%"},
            persistence='string',
            persistence_type='memory')            
            ], 
            
            style={'width': '30%', 'background-color': '#8B000000'}, className='box'),
    
        html.Div([
            dcc.Graph(id = 'line_graph'),
            ],style={'width': '70%'}, className='box'),
        
        ], style={'display': 'flex', 
                 'background-image':'url(https://st3.idealista.pt/news/arquivos/styles/news_detail/public/2020-07/denise-jans-oavjqz-nfd0-unsplash.jpg?sv=JkD9EvJB&itok=UiyQ_mjj)'}
        ),
    
    html.Br(),
    
    html.Div([

        html.Br(),
    
        html.Div([
            html.Div([
                html.H2('Where are the most rated movies?'),
                dcc.Graph(id='choro_graph', style={'display': 'inline-block'})
                ], className="six columns"),

            html.Div([
                html.H2('Do you want to know the best movies released by year? Just check them!'),
                dcc.Graph(id='sunburst_graph', style={'display': 'inline-block'})
            ], className="six columns"),
        ], className="row"),
        
        dcc.Slider(id='year_slider',
                   min=df.Year.min(),
                   max=df.Year.max(),
                   marks={str(i): '{}'.format(str(i)) for i in
                   [1990, 1995, 2000, 2005, 2010, 2014]},
                   value=df.Year.min(),
                   dots=True,
                   step=1,
                   tooltip={'always visible':False,  # show current slider values
                            'placement':'bottom'},
                  )
    
    ]),
    html.H6('Group AR: Gustavo Tourinho(20180846) | João Henriques(20200670) | João Chaves(20200627) | Mohamed Elbawab(20201102)  ', style={ 'text-align': 'center'}),
])

####################Callbacks#######################

@app.callback(
    [dash.dependencies.Output('line_graph', 'figure'),
     dash.dependencies.Output('sunburst_graph', 'figure'),
     dash.dependencies.Output('choro_graph', 'figure')],
    [dash.dependencies.Input("country_drop", "value"),
     dash.dependencies.Input("company_drop", "value"),
     dash.dependencies.Input("genre_drop", "value"),
     dash.dependencies.Input("year_slider", "value")
     ]
)


def plots(country,company, genre,year):
    
    #First plot
    new_df = df.loc[(df['Country'] == country) & (df['Genre'] == genre) & (df['Company'] == company)]
    revenue_df = new_df.groupby(by = ['Year'])['Gross','Budget'].sum()
    line = px.line(revenue_df, x=revenue_df.index, y=revenue_df.columns, title = 'Which Country has the highest revenue by category?')
    
    #Second plot
    sun_df = df.loc[(df.Year == year)].set_index('Star').groupby(['Genre'])['Score'].nlargest(1).to_frame().reset_index()
    sun = px.sunburst(
                       data_frame =sun_df,
                       path = ['Score','Star','Genre'],
                       color = 'Genre',
                       color_discrete_sequence=px.colors.qualitative.Pastel 
                        )
    
    #Third plot
    choro_df = df.loc[(df.Year == year) & (df.Genre == genre)]
    
    choro = px.choropleth(choro_df, locations="Country", color='Score', 
                    locationmode='country names',
                    range_color=[0,10],
                    color_continuous_scale=px.colors.sequential.speed
                   )
    choro.update_layout(margin=dict(l=0, r=0, t=100, b=100))
    
    
    return line, sun, choro


################################# SECOND TAB #################################


df_II = pd.read_csv('movies.csv',encoding='ISO-8859-1')

df_gp_gross = df_II.groupby(['country', 'genre', 'year'])['gross'].sum().reset_index()
df_gp_score = df_II.groupby(['country', 'genre', 'year'])['score'].mean().reset_index()
df_gp = df_gp_gross.merge(df_gp_score)


country_options = [
    dict(label='Country ' + country, value=country)
    for country in df_II['country'].unique()]

genre_options = [
    dict(label='Genre ' + genre , value=genre)
    for genre in df_II['genre'].unique()]


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
        labelStyle={'display': 'block'},
        style={ 'color': '#ffffff'}
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


tab_2_layout = html.Div([

    #html.H1('Exploring Genres in Movie Industry', style={ 'text-align': 'center'}), #'background-color': '#000000',
    html.Div([
        html.Div([
            html.Br(),
            html.H1('Please select a Country', style={'text-align': 'left', 'font-weight': 'bold',
                                                      'font-size': '22px', 'color': '#ffffff'}), #'background-color': '#000000',
            dropdown_country,
            html.Br(),
            html.H1('Please select one or more Genre(s)', style={'text-align': 'left', 'font-weight': 'bold',
                                                    'font-size': '22px', 'color': '#ffffff'}),#'background-color': '#000000', 
            dropdown_genre,
            html.Br(),
            radio_moviedata,
            year_slider
        ], style={'width': '30%', 'background-color': '#8B000000'}, className='box'),

        html.Div([
            dcc.Graph(id='graph_example'),
        ], style={'width': '70%', 'background-color': '#8B000000'}, className='box'),
            html.Br(),
            html.Br(),

    
    ], style={'display': 'flex',
              'background-image':'url(https://st3.idealista.pt/news/arquivos/styles/news_detail/public/2020-07/denise-jans-oavjqz-nfd0-unsplash.jpg?sv=JkD9EvJB&itok=UiyQ_mjj)'}),


    html.Div([
        #html.Br(),
        #html.Br(),
        html.Div([
            html.H5('Top 10 Movies by Gross Revenue', style={'text-align': 'center'}),
            dcc.Graph(id='graph_example2'),
        ], style={'width': '50%', 'background-color': '#8B000000'}, className='box'),

        html.Div([
            html.H5('Top 10 Movies by Score', style={'text-align': 'center'}),
            dcc.Graph(id='graph_example3'),
        ], style={'width': '50%', 'background-color': '#8B000000'}, className='box'),

    
    ], style={'display': 'flex'}),
    
    html.H6('Group AR: Gustavo Tourinho(20180846) | João Henriques(20200670) | João Chaves(20200627) | Mohamed Elbawab(20201102)  ', style={ 'text-align': 'center'}),
])


@app.callback(
    Output('graph_example', 'figure'),
    [Input('country_drop', 'value'),
     Input('genre_drop', 'value'),
     Input('moviedata_radio', 'value'),
     Input('year_slider', 'value')]
)
def update_graph(countries,genres, moviedata, year):
    
    filtered_by_year_df = df_gp[(df_gp['year'] >= year[0]) & (df_gp['year'] <= year[1])]

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



@app.callback(
    Output('graph_example2', 'figure'),
    [Input('country_drop', 'value'),
     Input('genre_drop', 'value'),
     Input('moviedata_radio', 'value'),
     Input('year_slider', 'value')]
)


def update_graph2(countries,genres, moviedata, year):
    filtered_by_year_df = df_II[(df_II['year'] >= year[0]) & (df_II['year'] <= year[1])]

    scatter_data = []

    for country in countries:
        filtered_by_year_and_country_df = filtered_by_year_df.loc[filtered_by_year_df['country'] == country]
        
    for genre in genres:
        filtered_by_year_and_country_and_genre_df = filtered_by_year_and_country_df.loc[filtered_by_year_and_country_df['genre'] == genre]

    top10 = filtered_by_year_and_country_and_genre_df.nlargest(10, "gross")
    top10.sort_values("gross", ascending = True, inplace = True)
    
    fig2 = px.bar(top10, x='gross', y='name', color="gross")

    
    return fig2

@app.callback(
    Output('graph_example3', 'figure'),
    [Input('country_drop', 'value'),
     Input('genre_drop', 'value'),
     Input('moviedata_radio', 'value'),
     Input('year_slider', 'value')]
)

def update_graph3(countries,genres, moviedata, year):
    filtered_by_year_df = df_II[(df_II['year'] >= year[0]) & (df_II['year'] <= year[1])]


    for country in countries:
        filtered_by_year_and_country_df = filtered_by_year_df.loc[filtered_by_year_df['country'] == country]
        
    for genre in genres:
        filtered_by_year_and_country_and_genre_df = filtered_by_year_and_country_df.loc[filtered_by_year_and_country_df['genre'] == genre]
    
    top10 = filtered_by_year_and_country_and_genre_df.nlargest(10, "score")
    top10.sort_values("score", ascending = True, inplace = True)
    
    fig3 = px.bar(top10, x='score', y='name', color="score")

    
    return fig3


################################# CONT. APP #################################


app.layout = html.Div([
    html.H1('Movie Industry: Guide through the evolution of 7th Art!🎬'),
    dcc.Tabs(id="tabs-example", value='tab-1-example', children=[
        dcc.Tab(label='Scene One 🎬', value='tab-1-example'),
        dcc.Tab(label='Scene Two 🎬', value='tab-2-example'),
    ]),
    html.Div(id='tabs-content-example')
])

@app.callback(Output('tabs-content-example', 'children'),
              [Input('tabs-example', 'value')])
def render_content(tab):
    if tab == 'tab-1-example':
        return tab_1_layout
    elif tab == 'tab-2-example':
        return tab_2_layout

# Tab 1 callback
@app.callback(dash.dependencies.Output('page-1-content', 'children'),
              [dash.dependencies.Input('page-1-dropdown', 'value')])
def page_1_dropdown(value):
    return 'You have selected "{}"'.format(value)

# Tab 2 callback
@app.callback(Output('page-2-content', 'children'),
              [Input('page-2-radios', 'value')])
def page_2_radios(value):
    return 'You have selected "{}"'.format(value)

app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})


if __name__ == '__main__':
    app.run_server(debug=False)
