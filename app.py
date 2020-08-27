#https://github.com/austinlasseter/flying-dog-beers
#https://github.com/dobothor/spatial-gini


import dash

from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import gunicorn
import pandas
import dash_table

global G
#G = pandas.read_csv(r"C:\Users\Thor\Dropbox\dashboard\web-app\G_new.csv")
url = "https://raw.githubusercontent.com/dobothor/spatial-gini/master/G_new.csv"
G = pandas.read_csv(url)
G.iloc[0:111,1:33]=G.iloc[0:111,1:33].applymap(lambda x: round(x,3))
#could use better way to round numbers...
print(G.head())
url = "https://raw.githubusercontent.com/dobothor/spatial-gini/master/issue.csv"
I = pandas.read_csv(url)

global c
c=1

#this part establishes the server
app = dash.Dash(__name__)
server = app.server


###############

#this establishes the layout, work here to add components
app.layout = html.Div([
    html.H1(children="Select an Industry to see the Spatial Gini over time"),
    dcc.Dropdown(
        id='demo-dropdown',     #it doesn't preserve spaces at start, ...
        options=[{'label': i, 'value': i} for i in G['Industry']],
        multi=True
    ),
    html.Div(id='dd-output-container'),
    dcc.Graph(id='Spatial-Gini',
              config={'scrollZoom':True}
              ),
    html.H2("The spatial gini is constructed using the earnings per county " +
            "for each industry, from the BEA dataset CAINC5S"),
    html.H2("To protect the confidentiality of regional businesses " +
            "many of the county observations are censored as shown below"),
    dcc.Graph(id='Data Suppression',
              config={'scrollZoom':True}
              ),

    dash_table.DataTable(
        id='Table',
        columns=[{"name":i, "id":i} for i in G.columns],
        data=G.to_dict('records'),
        ),
])

# Additional Ideas
# -print suppression % as bar chart below
# -color the table https://dash.plotly.com/datatable/conditional-formatting
# -help guide to click for explanation of spatial Gini (pic of cumulative)
################


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
    if value==None:
        return{}
    traces = []
    for i in value:
        idx = list(G['Industry']).index(i)
        df = G.iloc[idx,]
        traces.append(
            go.Scatter(x =[i for i in range(1969,2001)],
                       y = list(df.iloc[1:33]),
                       name=i
                       )
            )
    return {
        'data': traces,      #name of lines is based on trace index
        'layout': go.Layout(
            title="Spatial-Gini",
            ),
        }
#this controls the data suppression bar chart
@app.callback(
    dash.dependencies.Output('Data Suppression', 'figure'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_graph(value):
    if value==None:
        return{}
    traces = []
    for i in value:
        idx = list(I['Industry']).index(i)
        df = I.iloc[idx,]
        traces.append(
            go.Bar(x =[i for i in range(1969,2001)],
                       y = list(df.iloc[1:33]),
                       name=i
                       )
            )
    return {
        'data': traces,      #name of lines is based on trace index
        'layout': go.Layout(
            title="Data Suppression % of Counties",
            ),
        }
        
    

#################
#this is the ongoing run loop
if __name__ == '__main__':
    
    app.run_server(debug=True)
