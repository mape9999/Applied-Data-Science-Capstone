

import dash
from dash import dcc, html
from dash.dependencies import Output, Input
import pandas as pd
import plotly.express as px

# Load the data from CSV
df = pd.read_csv('spacex_launch_geo.csv')
print(df.columns)

# Extract unique launch site names
launch_sites = df['Launch Site'].unique()

# Define dropdown options (including the "All Sites" option)
dropdown_options = [{'label': 'All Sites', 'value': 'ALL'}] + \
                   [{'label': site, 'value': site} for site in launch_sites]

# Define payload range
min_payload = 0
max_payload = 10000

# Define the RangeSlider
payload_slider = dcc.RangeSlider(
    id='payload-slider',
    min=min_payload,
    max=max_payload,
    step=1000,
    marks={i: str(i) for i in range(min_payload, max_payload + 1000, 2000)},
    value=[min_payload, max_payload]
)

# Initialize Dash app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div([
    html.H4("Select a Launch Site:"),
    dcc.Dropdown(
        id='site-dropdown',
        options=dropdown_options,
        value='ALL',
        placeholder='Select a Launch Site',
        searchable=True,
        clearable=False
    ),
    
    html.Br(),

    html.H4("Select Payload Range (Kg):"),
    payload_slider,

    html.Br(),
    
    dcc.Graph(id='success-pie-chart'),  

    html.Br(),
    
    dcc.Graph(id='success-payload-scatter-chart')  
    ])

# Correct Callback for the Pie Chart
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_piechart(entered_site):
    if entered_site == 'ALL':
        success_counts = df[df['class'] == 1].groupby('Launch Site').size().reset_index(name='count')

        fig = px.pie(success_counts, values='count', names='Launch Site',
                     title='Total Successful Launches (All Sites)')
    else:
        filtered_df = df[df['Launch Site'] == entered_site]
        success_counts = filtered_df['class'].value_counts().reset_index()
        success_counts.columns = ['class', 'count']

        success_counts['class'] = success_counts['class'].map({0: 'Failure', 1: 'Success'})

        fig = px.pie(success_counts, values='count', names='class',
                     title=f'Success vs Failure for {entered_site}')

    return fig

#  Callback for the Scatter Plot
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def update_scatter_chart(selected_site, selected_payload):
    # Filter data based on payload range
    filtered_df = df[(df['Payload Mass (kg)'] >= selected_payload[0]) & 
                     (df['Payload Mass (kg)'] <= selected_payload[1])]

    if selected_site == 'ALL':
        fig = px.scatter(
            filtered_df, 
            x='Payload Mass (kg)', 
            y='class',
            color='Booster Version',  # Color points by booster version
            size_max=10,
            opacity=0.8,
            title="Payload vs. Mission Outcome for All Sites",
            labels={'class': 'Launch Outcome (0 = Failure, 1 = Success)'}
        )
    else:
        # Filter for the selected site
        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]

        fig = px.scatter(
            filtered_df, 
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version',
            size_max=10,
            opacity=0.8,
            title=f"Payload vs. Mission Outcome for {selected_site}",
            labels={'class': 'Launch Outcome (0 = Failure, 1 = Success)'}
        )

    return fig

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)