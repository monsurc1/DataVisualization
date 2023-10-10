import pandas as pd
import dash
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objs as go
from dash.dependencies import Input, Output

# Load data from CSV file
df = pd.read_csv('SwissGDP_Final2.csv')
# new dataframe for the pie-chart
df_new = df.drop([0, 5, 6])

# for heatmap
df_hmap = df.drop([0, 1, 2, 3, 4])
df_hmap = df_hmap.rename(index={6: 'Unemployment(% of total labor force)'})
#print(df_hmap.index[1])

# Define slider marks
slider_ticks = {str(i): str(i) for i in range(2012, 2022)}

# Define slider component
slider = dcc.Slider(
    id="year-slider",
    min=2012,
    max=2021,
    step=1,
    marks=slider_ticks,
    value=2012,
    className="mt-5 mb-5",
)

# Create the heatmap trace - Heatmap section starts here
trace = go.Heatmap(
    x=df_hmap.columns[2:],
    y=df_hmap['Indicator Name'],
    z=df_hmap.iloc[:, 2:].values,
    text=[['{:.2f}%'.format(val) for val in row] for row in df_hmap.iloc[:, 2:].values],
    colorscale='YlOrRd',
    zmin=df_hmap.iloc[:, 2:].values.min(),
    zmax=df_hmap.iloc[:, 2:].values.max(),
    colorbar=dict(
        title='Value',
        tickprefix='',
    )
)

# Create the layout
layout = go.Layout(
    #title='Heatmap Example',
    xaxis=dict(title='Year'),
    yaxis=dict(title='Indicator Name'),
)

# Create the figure
fig = go.Figure(data=[trace], layout=layout)

# Convert the figure to a Plotly Dash component
graph = dcc.Graph(
    id='heatmap',
    figure=fig,
)  # Heatmap setup ends here.

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(style={'backgroundColor': '#eeedeb82'}, children=[
    html.H1(children='Swiss GDP at a glance', style={'textAlign': 'center', 'color': 'brown', 'background-color':'bisque'}),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.P("Swiss GDP over the last 5 years", style={'textAlign': 'center'}),
                dcc.Graph(
                    id='gdp-line-plot',
                    figure={
                        'data': [
                            {'x': df.columns[2:],
                             'y': df[df['Indicator Name'] == 'GDP (constant LCU)'].iloc[0, 2:].values, 'type': 'line'}
                        ],
                        'layout': {
                            #'title': 'Swiss GDP over the last 5 years',
                            'xaxis': {'title': 'Year'},
                            'yaxis': {'title': 'GDP (constant LCU)'}
                        }
                    }
                )
            ])
        ),
        dbc.Col(
            html.Div([
                html.P("Select GDP indicators from the dropdown", style={'textAlign': 'center'}),
                dcc.Dropdown(
                    id='indicator-dropdown',
                    options=[{'label': i, 'value': i} for i in df['Indicator Name'].unique()[1:]],
                    value='GDP (constant LCU)'
                ),
                dcc.Graph(
                    id='gdp-bar-chart',
                    figure={
                        'data': [
                            {'x': df.columns[2:],
                             'y': df[df['Indicator Name'] == 'GDP (constant LCU)'].iloc[0, 2:].values, 'type': 'bar'}
                        ],
                        'layout': {
                            'title': 'Swiss GDP (constant LCU)',
                            'xaxis': {'title': 'Year'},
                            'yaxis': {'title': 'GDP (constant LCU)'}
                        }
                    }
                )
            ])
        ),
    ]),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H1('Heatmap', style={'textAlign': 'center'}),
                html.P('Heatmap on Swiss Unemployment and Inflation.', style={'textAlign': 'center'}),
                graph
            ]),
            width=6,
            style={'backgroundColor': 'white'}
        ),
        dbc.Col(
            html.Div([
                html.H1("Pie Chart", style={'textAlign': 'center'}),
                dcc.Graph(
                    id="pie-chart",
                    figure={},
                    config={"displayModeBar": False},
                ),
                slider,
            ]), width=6,
        ),
    ]),
    dbc.Row([
            dbc.Col([
                    dash_table.DataTable(
                        id='table',
                        columns=[{"name": i, "id": i} for i in df.columns],
                        data=df.to_dict('records')
                    )
            ]),
        ], align="center"),
])


@app.callback(Output('gdp-bar-chart', 'figure'),
              Input('indicator-dropdown', 'value'))
def update_bar_chart(indicator):
    data = [{'x': df.columns[2:], 'y': df[df['Indicator Name'] == indicator].iloc[0, 2:].values, 'type': 'bar'}]
    layout = {
        'title': 'Swiss ' + indicator + ' over time',
        'xaxis': {'title': 'Year'},
        'yaxis': {'title': indicator}
    }
    return {'data': data, 'layout': layout}


# Define app callback for the Pie-chart
@app.callback(
    Output("pie-chart", "figure"),
    [Input("year-slider", "value")],
)
def update_pie_chart(selected_year):
    # Filter data by selected year
    df_filtered = df_new[df_new[str(selected_year)] != ""]

    # Create pie chart
    fig = px.pie(
        df_filtered,
        names="Indicator Name",
        values=str(selected_year),
        title=f"Year: {selected_year}",
    )

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
