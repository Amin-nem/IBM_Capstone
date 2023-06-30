# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),

    # Task 1: Add a dropdown list to enable Launch Site selection
    html.Div([
        dcc.Dropdown(id='site-dropdown',
                     options=[{'label': site, 'value': site.lower()} for site in spacex_df['Launch Site'].unique()],
                     value='ALL',
                     placeholder='Select a Launch Site here',
                     searchable=True)
    ]),

    html.Br(),

    # Task 2: Add a pie chart to show the total successful launches count for all sites
    # If a specific launch site was selected, show the Success vs. Failed counts for the site
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),

    # Task 3: Add a slider to select payload range
    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=10000,
        step=1000,
        value=[min_payload, max_payload],
        marks={i: str(i) for i in range(0, 10001, 1000)}
    ),

    # Task 4: Add a scatter chart to show the correlation between payload and launch success
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])


# Task 2: Add a callback function to render success-pie-chart based on selected site dropdown
@app.callback(Output('success-pie-chart', 'figure'),
              Input('site-dropdown', 'value'))
def update_pie_chart(site):
    if site == 'ALL':
        data = spacex_df.groupby('class').size().reset_index(name='counts')
        fig = px.pie(data, values='counts', names='class', title='Total Success Launches By Class')
    else:
        site_df = spacex_df[spacex_df['Launch Site'] == site]
        data = site_df.groupby('class').size().reset_index(name='counts')
        fig = px.pie(data, values='counts', names='class', title=f"Total Success Launches for Site {site}")
    return fig


# Task 4: Add a callback function to render the success-payload-scatter-chart scatter plot
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id="payload-slider", component_property="value")])
def update_scatter_chart(site, payload):
    if site == 'ALL':
        filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload[0]) & (spacex_df['Payload Mass (kg)'] <= payload[1])]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category',
                         title='Correlation between Payload and Success for all Sites')
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == site]
        filtered_df = filtered_df[(filtered_df['Payload Mass (kg)'] >= payload[0]) & (filtered_df['Payload Mass (kg)'] <= payload[1])]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category',
                         title=f'Correlation between Payload and Success for Site {site}')
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server()