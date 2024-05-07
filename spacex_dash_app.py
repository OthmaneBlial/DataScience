import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

spacex_df = pd.read_csv("spacex_launch_dash.csv")
min_payload, max_payload = spacex_df['Payload Mass (kg)'].agg(['min', 'max'])

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('SpaceX Launch Records Dashboard', style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    dcc.Dropdown(
        id='site-dropdown', 
        options=[{'label': 'All Sites', 'value': 'All Sites'}] + [{'label': site, 'value': site} for site in spacex_df["Launch Site"].unique()],
        value='All Sites', 
        placeholder="Select a Launch Site here", 
        searchable=True
    ),
    html.Br(),
    dcc.Graph(id='success-pie-chart'),
    html.Br(),
    html.P("Payload range (Kg):"),
    dcc.RangeSlider(
        id='payload-slider', 
        min=0, 
        max=10000, 
        step=1000, 
        value=[min_payload, max_payload], 
        marks={x: {'label': str(x) + ' (Kg)'} for x in range(2500, 10001, 2500)}
    ),
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# Callback for update the pie chart
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def update_pie_chart(site):
    if site == 'All Sites':
        fig = px.pie(spacex_df, values='class', names='Launch Site', title='Total Success Launches by Site')
    else:
        fig = px.pie(spacex_df[spacex_df["Launch Site"] == site], values='class', names='class', title='Total Success Launches for ' + site)
    return fig

# Callback for update the scatter chart
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'), Input('payload-slider', 'value')]
)
def update_scatter_chart(site, payload_range):
    filtered_df = spacex_df[(spacex_df["Payload Mass (kg)"] >= payload_range[0]) & (spacex_df["Payload Mass (kg)"] <= payload_range[1])]
    if site != 'All Sites':
        filtered_df = filtered_df[filtered_df["Launch Site"] == site]
    fig = px.scatter(
        filtered_df, 
        y="class", 
        x="Payload Mass (kg)", 
        color="Booster Version Category",
        title=f"Correlation between Payload and Launch Success for {site}"
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
