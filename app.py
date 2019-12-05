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
    style={'float': 'left',
           'width': '45vw',
           'height': '45vw',
           'paddingLeft': '1vw'}
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
    style={'float': 'right',
           'width': '45vw',
           'height': '45vw',
           'paddingRight': '1vw'}
)

# creates div for text descring project
text_div = html.Div(
    children=[html.H1(['Us Energy Generation']),
              html.H2(['A data visualization project by Sean Antosiak']),
              html.H3(['Data from the Energy Information Administration']),
              html.Div([''''''])  # maybe I will add further description later
              ],
    style={'float': 'top'}
)

# creates instance of dash app
app = dash.Dash()

# sets the layout for the app
app.layout = html.Div([text_div, map_div, line_div])


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

    # update map to limit the scope to only include US
    fig_map.update_layout(title='Us Energy Generation By State',
                          geo_scope='usa')

    return(fig_map)


@app.callback(
    Output('line', 'figure'),
    [Input('sourceChecklist', 'value')])
def createLine(sourceChecklist):

    # creates new df that just includes totals for all US states combined
    us = gen[gen['STATE'] == 'US'].copy()

    # creates a blank plotly figure and sets axis titles
    fig_line = go.Figure()
    fig_line.update_layout(title='Energy Produced By Year (US Total)',
                           xaxis_title='Year',
                           yaxis_title='Megawatt hours')

    # creates a dictionary to change line color based on source
    colorDict = {'Total': 'magenta',
                 'Coal': 'black',
                 'Natural Gas': 'blue',
                 'Petroleum': 'brown',
                 'Nuclear': 'green',
                 'Wind': 'grey',
                 'Hydroelectric Conventional': 'cyan',
                 'Solar Thermal and Photovoltaic': 'orange'
                 }

    # creates a trace for each source checked in the checklist
    for source in sourceChecklist:
        source_df = us[us['SOURCE'] == source]
        fig_line.add_trace(go.Scatter(
            x=source_df['YEAR'],
            y=source_df['Mwh'],
            mode='lines+markers',
            name=f'{source}',
            marker_color=f'{colorDict[source]}'
        ))

    return(fig_line)


if __name__ == '__main__':
    app.run_server(debug=True)
