import pandas as pd
import dash
from dash import Dash, dcc, html, callback
from dash.dependencies import Input, Output, State
import plotly.express as px
from dash import dash_table
import dash_bootstrap_components as dbc

df = pd.read_csv('climate_new.csv')

# Average monthly temperature in Berlin, Vienna, Bern and Luxembourg over the last year

fig = px.bar(df, x='month', y='avgtemp_c', color='city', title="Average monthly temperature",
             barmode='group', height=400)
    
    
fig = fig.update_layout(
        plot_bgcolor="#222222", paper_bgcolor="#222222", font_color="white"
    )
graph = dcc.Graph(figure=fig)

# Plot a minimum monthly temperature in cities

fig2 = px.line(df, x='month', y='mintemp_c', title="Minimum monthly temperature", color='city', height=400)
fig2 = fig2.update_layout(
        plot_bgcolor="#222222", paper_bgcolor="#222222", font_color="white"
    )
graph2 = dcc.Graph(figure=fig2)

# Plot a max wind speed in cities

fig3 = px.bar(df, x='month', y='maxwind_kph', color='city',title="Maximum wind speed",
             barmode='group', height=400)

fig3 = fig3.update_layout(
        plot_bgcolor="#222222", paper_bgcolor="#222222", font_color="white"
    )
graph3 = dcc.Graph(figure=fig3)

# Plot a minimum monthly temperature in cities

fig4 = px.line(df, x='month', y='avghumidity', title="Average monthly humidity", color='city', height=400)
fig4 = fig4.update_layout(
        plot_bgcolor="#222222", paper_bgcolor="#222222", font_color="white"
    )
graph4 = dcc.Graph(figure=fig4)

df2 = pd.read_csv('climate_raw.csv', parse_dates = ['date'])
# Count the occurrences of 'rain' in the 'weather_conditions' column
df2['rain_count'] = df2['condition'].str.lower().str.count('rain')

# Group by 'city' and sum the 'rain_count' for each city
result_df = df2.groupby('city')['rain_count'].sum().reset_index()

app =dash.Dash(external_stylesheets=[dbc.themes.DARKLY])

dropdown = dcc.Dropdown(['Berlin', 'Vienna', 'Bern', 'Luxembourg'], 'Berlin', clearable=False, multi=True, style ={'paddingLeft': '30px', 
                                                             "backgroundColor": "#222222", "color": "#222222"})


d_table = dash_table.DataTable(result_df.to_dict('records'),
                               columns=[
                                        {"name": "City", "id": "city"},
                                        {"name": "Rainy Days", "id": "rain_count"}
                                        ],
                               style_data={'color': 'white', 'backgroundColor': '#424242'},
                               style_cell={'padding': '5px'},
                               style_header={
                                  'backgroundColor': '#1976D2',
                                  'color': 'white','fontWeight': 'bold'},
                               style_table={ 
                                          'minHeight': '170px', 'height': '170px', 'maxHeight': '170px',
                                         'minWidth': '900px', 'width': '900px', 'maxWidth': '900px',
                                         'marginLeft': 'auto', 'marginRight': 'auto',
                                         'marginTop': 0, 'marginBottom': "30"},
                               style_cell_conditional=[
        {
            'if': {'column_id': c},
            'textAlign': 'center'
        } for c in ['city', 'rain_count']
    ])

# set app layout

app.layout = html.Div([html.H1('Best city to live', style={'textAlign': 'center', 'color': '#1976D2'}), 
                       html.H3('Number of rainy days per year', style={'fontSize': '24px'}),
                       html.Div([d_table, dropdown, graph, graph2, graph3, graph4])
])

@callback(
    Output(graph, "figure"), 
    Input(dropdown, "value"))

def update_bar_chart(selected_cities): 
    mask = df["city"].isin(selected_cities)
    fig =px.bar(df[mask], 
             x='month', 
             y='avgtemp_c',  
             color='city',
             barmode='group',
             height=400, title = "Average monthly temperature",)
    fig = fig.update_layout(
        plot_bgcolor="#222222", paper_bgcolor="#222222", font_color="white"
    )

    return fig

if __name__ == '__main__':
     app.run_server()

server = app.server