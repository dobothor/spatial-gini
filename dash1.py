
import dash

from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

import pandas

global G
G = pandas.read_csv(r"D:\thor's folder\grad stuff\Transpo\Transport Econ\data\BEA\clustering\G_new.csv")
print(G.head())

global c
c=1

#this part establishes the server
app = dash.Dash(__name__)
server = app.server


#this establishes the layout, work here to add components
app.layout = html.Div([
    dcc.Dropdown(
        id='demo-dropdown',
        options=[
            {'label': i, 'value': i} for i in G['Industry']
        ]
    ),
    html.Div(id='dd-output-container'),
    dcc.Graph(id='Spatial-Gini')
])

#this controls the dropdown menu interaction
#not actually necessary
@app.callback(
    dash.dependencies.Output('dd-output-container', 'children'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_output(value):
    global c
    c=c+1
    print("Of all the things!",c)
    return 'You have selected {}'.format(value)

#this controls the graph shown by the dropdown menu
@app.callback(
    dash.dependencies.Output('Spatial-Gini', 'figure'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_graph(value):
    idx = list(G['Industry']).index(value)
    df = G.iloc[idx,]

    trace = go.Scatter(x =[i for i in range(1969,2001)],
                       y = list(df.iloc[1:33])
                       )
    return {
        'data': [trace],
        'layout': go.Layout(
            title="Spatial-Gini for {}".format(value)
            )
        }
    
    

#################
#this is the ongoing run loop
if __name__ == '__main__':
    
    app.run_server(debug=False)