import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px
from dash.dependencies import Input, Output
from data import *

# creates div for the choropleth map
map_div = html.Div(
    children=[

        # takes map from appcallback
        dcc.Graph(id='map'),

        # creaes year slider
        html.Div(
            dcc.Slider(id='yearSlider',
                       min=1990,
                       max=2017,
                       step=1,
                       dots=True,
                       marks={1990: '1990', 1995: '1995', 2000: '2000',
                              2005: '2005', 2010: '2010', 2017: '2017'},
                       value=1990
                       ),
            # adds padding so slider and dropdown dont overlap
            style={'paddingBottom': '30px'}
        ),

        # creates dropdown for selecting source
        dcc.Dropdown(
            id='sourceDropdown',
            options=[
               {'label': 'Total', 'value': 'Total'},
               {'label': 'Coal', 'value': 'Coal'},
               {'label': 'Natural Gas', 'value': 'Natural Gas'},
               {'label': 'Petrolium', 'value': 'Petroleum'},
               {'label': 'Nuclear Power', 'value': 'Nuclear'},
               {'label': 'Hydroelectric Power',
                'value': 'Hydroelectric Conventional'},
               {'label': 'Wind', 'value': 'Wind'},
               {'label': 'Solar', 'value': 'Solar Thermal and Photovoltaic'},
            ],
            value='Total'
            ),
        ],
    # sets style to put map on left with padding
    style={'paddingLeft': '2%',
           'width': '40%',
           'float': 'left'}
)


# creates div for line graph
line_div = html.Div(
    children=[

        # takes line graph form appcallback
        dcc.Graph(id='line'),

        # creates checklist for sources
        dcc.Checklist(
            id='sourceChecklist',
            options=[
                {'label': 'Total', 'value': 'Total'},
                {'label': 'Coal', 'value': 'Coal'},
                {'label': 'Natural Gas', 'value': 'Natural Gas'},
                {'label': 'Petrolium', 'value': 'Petroleum'},
                {'label': 'Nuclear Power', 'value': 'Nuclear'},
                {'label': 'Hydroelectric Power',
                 'value': 'Hydroelectric Conventional'},
                {'label': 'Wind', 'value': 'Wind'},
                {'label': 'Solar',
                 'value': 'Solar Thermal and Photovoltaic'},
            ],
            value=['Total'],
            labelStyle={'display': 'inline-block',
                        'margin-left': '1em'}
        ),
    ],

    # sets style to put line graph on right with padding
    style={'paddingRight': '2%',
           'width': '50%',
           'float': 'right'}
)


# creates instance of dash app
app = dash.Dash()

app.layout = html.Div([map_div, line_div])


@app.callback(
    Output('map', 'figure'),
    [Input('sourceDropdown', 'value'),
     Input('yearSlider', 'value')])
def createMap(sourceDropdown, yearSlider):

    # removes US total from dataframe so colorscale works correctly
    genX = gen[gen['STATE'] != 'US']

    # creates dataframe based on input soure requested
    genX = genX[genX['SOURCE'] == f'{sourceDropdown}']

    # reduces dataframe to only the year selected
    genX = genX[genX['YEAR'] == yearSlider]

    # creates a dictionary to change colorscale based on source
    colorDict = {'Total': 'cividis',
                 'Coal': 'greys',
                 'Natural Gas': 'blues',
                 'Petroleum': 'earth',
                 'Nuclear': 'speed',
                 'Wind': 'darkmint',
                 'Hydroelectric Conventional': 'mint',
                 'Solar Thermal and Photovoltaic': 'solar'
                 }

    # creates a dictionary for the scale max of each source
    scaleDict = {'Total': 300000000,
                 'Coal': 100000000,
                 'Natural Gas': 150000000,
                 'Petroleum': 1000000,
                 'Nuclear': 50000000,
                 'Wind': 50000000,
                 'Hydroelectric Conventional': 50000000,
                 'Solar Thermal and Photovoltaic': 25000000
                 }

    # creates choropleth map from dataframe
    fig_map = go.Figure(data=go.Choropleth(
                        locations=genX['STATE'],
                        locationmode='USA-states',
                        z=genX['Mwh'],
                        colorscale=colorDict[sourceDropdown],
                        colorbar_title='Mwh',
                        zmin=0,
                        zmax=scaleDict[sourceDropdown]
                        ))

    # update map with title and limits scope to only include US
    fig_map.update_layout(
        title_text='State Energy Generation by selected Source and Year',
        geo_scope='usa'
    )

    return(fig_map)


@app.callback(
    Output('line', 'figure'),
    [Input('sourceChecklist', 'value')])
def createLine(sourceChecklist):

    # creates new df that just includes totals for all US states combined
    us = gen[gen['STATE'] == 'US'].copy()

    usdf = pd.DataFrame()
    for source in sourceChecklist:
        sourceDF = us[us['SOURCE'] == source]
        usdf = pd.concat([usdf, sourceDF])

    fig_line = px.line(usdf, x='YEAR', y='Mwh', color='SOURCE')

    return(fig_line)


if __name__ == '__main__':
    app.run_server(debug=True)
