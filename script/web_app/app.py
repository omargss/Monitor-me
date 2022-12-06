""" Python web app """
import configparser
import paramiko
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import functions
import plotly.graph_objects as go

app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
""" SERVER CONNECTION """
config = configparser.RawConfigParser()
config.read("../config.txt")
hostname = config['settings']['hostname']
port = config['settings']['port']
username = config['settings']['username']
password = config['settings']['password']

client = paramiko.SSHClient()
client.load_system_host_keys()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
client.connect(hostname = hostname, port=port, username=username, password=password)

memorylist = functions.get_memory(client)
""" MEMORY CHART """
data = {
        'Memory_Type': ['Total', 'Used', 'Free', 'Shared','Buff/Cache','Available'],
        'Memory': memorylist
        }
df = pd.DataFrame(data)
memoryGraph = px.bar(df, x="Memory_Type", y="Memory",
color="Memory_Type", title="Usage of the memory of the remote server", barmode='stack')
memoryGraph.update_layout(xaxis_title='Name')
""" LOGS CHART """
logs = functions.getAccessLogs(client)
labels = []
values = []
i=0
for log in logs:
    labels.append(log.name)
    values.append(log.numberOfSearchs)
    i+=1
logPieChart = go.Figure(data=[go.Pie(labels=labels, values=values)])

app.layout = html.Div(children=[
    html.H1(children='Monitoring web application'),
    html.H2(children='Memory'),

    dcc.Graph(
        id='Memory Graph',
        figure=memoryGraph
    ),
        html.H2(children='Logs'),
        dcc.Graph(
        id='Pie Logs chart',
        figure=logPieChart
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
