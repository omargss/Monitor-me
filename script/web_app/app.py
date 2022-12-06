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

""" MEMORY CHART """
memorylist = functions.get_memory(client)
memorydata = {
        'Memory_Type': ['Total', 'Used', 'Free', 'Shared','Buff/Cache','Available'],
        'Memory': memorylist
        }
df = pd.DataFrame(memorydata)
memoryGraph = px.bar(df, x="Memory_Type", y="Memory",
color="Memory_Type", title="Usage of the memory of the remote server", barmode='stack')
memoryGraph.update_layout(xaxis_title='Name')
""" LOGS CHART """
logs = functions.getAccessLogs(client)
memory_labels = []
memory_values = []
for log in logs:
    memory_labels.append(log.name)
    memory_values.append(log.numberOfSearchs)
logPieChart = go.Figure(data=[go.Pie(labels=memory_labels, values=memory_values)])
""" PROCESSES CHART """
processlist = functions.getProcessInfos(client)
process_labels = []
process_values = []
for process in processlist:
    process_labels.append(process.command)
    process_values.append(10)
processPieChart = go.Figure(data=[go.Pie(labels=process_labels, values=process_values)])
""" WEB DISPLAY """
app.layout = html.Div(children= [
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
    ),
    html.H2(children='Processes'),
    dcc.Graph(
        id='Pie process chart',
        figure=processPieChart
    ),
])

if __name__ == '__main__':
    app.run_server(debug=True)
