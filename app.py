import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from GenerationData import *

app = dash.Dash()


app.layout = html.Div(children=[
    html.H1('United States Energy Generation'),

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

    dcc.Graph(id='map'),

    dcc.Slider(id='yearSlider',
               min=1990,
               max=2017,
               step=1,
               dots=True,
               marks={1990: '1990', 1995: '1995', 2000: '2000',
                      2005: '2005', 2010: '2010', 2017: '2017'},
               value=1990
               )
])


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

    # creates choropleth map from dataframe
    fig = go.Figure(
              data=go.Choropleth(
                  locations=genX['STATE'],
                  locationmode='USA-states',
                  z=genX['Mwh'],
                  colorscale=colorDict[sourceDropdown],
                  colorbar_title='Mwh'
              ))

    # update map with title and limits scope to only include US
    fig.update_layout(
        title_text='State Energy Generation by selected Source and Year',
        geo_scope='usa'
    )

    return(fig)


if __name__ == '__main__':
    app.run_server(debug=True)
