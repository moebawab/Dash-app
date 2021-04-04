import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd
import tab1
import tab2

# Dataset Processing

#path = 'https://raw.githubusercontent.com/nalpalhao/DV_Practival/master/datasets/'

#df = pd.read_csv(path + 'emissions.csv')

df = pd.read_csv('movies.csv',encoding='latin1')

# The app itself

app = dash.Dash(__name__, external_stylesheets='')
server = app.server

app.config['suppress_callback_exceptions'] = True

app.layout = html.Div([
    html.H1('Dash Tabs component demo'),
    dcc.Tabs(id="tabs-example", value='tab-1-example', children=[
        dcc.Tab(label='Tab One', value='tab-1-example'),
        dcc.Tab(label='Tab Two', value='tab-2-example'),
    ]),
    html.Div(id='tabs-content-example')
])



@app.callback(Output('tabs-content-example', 'children'),
              [Input('tabs-example', 'value')])
def render_content(tab):
    if tab == 'tab-1-example':
        return tab1.tab1_layout
    elif tab == 'tab-2-example':
        return tab2.tab2_layout

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
    

#    fig2 =px.bar(scatter_data, layout=scatter_layout)#x='gross', y='genre')
    
#    fig2 = px.scatter(df, x="gross", y="director",
#                      size="score", color="genre", hover_name="company",
#                 log_x=True, size_max=60)
    
    return fig



@app.callback(
    Output('graph_example2', 'figure'),
    [Input('country_drop', 'value'),
     Input('genre_drop', 'value'),
     Input('moviedata_radio', 'value'),
     Input('year_slider', 'value')]
)


def update_graph2(countries,genres, moviedata, year):
    filtered_by_year_df = df[(df['year'] >= year[0]) & (df['year'] <= year[1])]

    scatter_data = []

    for country in countries:
        filtered_by_year_and_country_df = filtered_by_year_df.loc[filtered_by_year_df['country'] == country]
        
    for genre in genres:
        filtered_by_year_and_country_and_genre_df = filtered_by_year_and_country_df.loc[filtered_by_year_and_country_df['genre'] == genre]
    
#        temp_data = dict(
#            type='scatter',
#            y=filtered_by_year_and_country_and_genre_df[moviedata],
#            x=filtered_by_year_and_country_and_genre_df['gross'],
#            name=country+ genre
#        )

#        scatter_data.append(temp_data)

#    scatter_layout = dict(xaxis=dict(title='gross'),
#                          yaxis=dict(title=moviedata)
#                          )
    top10 = filtered_by_year_and_country_and_genre_df.nlargest(10, "gross")
    top10.sort_values("gross", ascending = True, inplace = True)
    
    fig2 = px.bar(top10, x='gross', y='name')

    
    return fig2

@app.callback(
    Output('graph_example3', 'figure'),
    [Input('country_drop', 'value'),
     Input('genre_drop', 'value'),
     Input('moviedata_radio', 'value'),
     Input('year_slider', 'value')]
)

def update_graph3(countries,genres, moviedata, year):
    filtered_by_year_df = df[(df['year'] >= year[0]) & (df['year'] <= year[1])]

#    scatter_data = []

    for country in countries:
        filtered_by_year_and_country_df = filtered_by_year_df.loc[filtered_by_year_df['country'] == country]
        
    for genre in genres:
        filtered_by_year_and_country_and_genre_df = filtered_by_year_and_country_df.loc[filtered_by_year_and_country_df['genre'] == genre]
    
#        temp_data = dict(
#            type='scatter',
#            y=filtered_by_year_and_country_and_genre_df[moviedata],
#            x=filtered_by_year_and_country_and_genre_df['gross'],
#            name=country+ genre
#        )

#        scatter_data.append(temp_data)

#    scatter_layout = dict(xaxis=dict(title='gross'),
#                          yaxis=dict(title=moviedata)
#                          )
    top10 = filtered_by_year_and_country_and_genre_df.nlargest(10, "score")
    top10.sort_values("score", ascending = True, inplace = True)
    
    fig3 = px.bar(top10, x='score', y='name')

    
    return fig3


#def generate_table(df, max_rows=10):
#    return html.Table([
#        html.Thead(
#            html.Tr([html.Th(col) for col in df.columns])
#        ),
#        html.Tbody([
#            html.Tr([
#                html.Td(df.iloc[i][col]) for col in df.columns
#            ]) for i in range(min(len(df), max_rows))
#        ])
#    ])
#    return table

if __name__ == '__main__':
    app.run_server(debug=False)
