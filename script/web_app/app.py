""" Python web app """
# pylint: disable=pointless-string-statement
# pyling: disable=unused-argument
import configparser
import time
import paramiko
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import functions

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
client.connect(hostname=hostname, port=port,
               username=username, password=password)

""" WEB DISPLAY """
app.layout = html.Div(children=[
    html.H1(children='Monitoring web application'),
    html.Div([
    html.Label('Hostname'),
    dcc.Input(id='hostname', value=hostname,type='text'),
    html.Label('port'),
    dcc.Input(id='port', value=port,type='text'),
    html.Label('username'),
    dcc.Input(id='username', value= username, type='text'),
    html.Label('password'),
    dcc.Input(id='password', value=password, type='password'),
    html.Button('Connection', id='btnConnection'),
]),
    html.H2(children='Memory'),
    dcc.Graph(
        id='Memory_pie_chart',
    ),
    html.H2(children='Biggest_files'),
    dcc.Graph(
        id='File_size_graph',
    ),
    html.H2(children='Processes'),
    dcc.Graph(
        id='Pie_process_chart',
    ),
    html.H2(children='Logs'),
    dcc.Graph(
        id='Logs_graph',
    ),
    html.H2(children='Error Logs'),
    dcc.Graph(
        id='Error_logs_graph',
    ),
    dcc.Interval(
            id='interval-component_memory',
            interval=20*1000, # in milliseconds
            n_intervals=0
        ),
    dcc.Interval(
            id='interval-component_files',
            interval=100*1000, # in milliseconds
            n_intervals=0
        ),
    dcc.Interval(
            id='interval-component_process',
            interval=20*1000, # in milliseconds
            n_intervals=0
        ),
    dcc.Interval(
            id='interval-component_logs',
            interval=20*1000, # in milliseconds
            n_intervals=0
        ),

    dcc.Interval(
            id='interval-component_error_logs',
            interval=20*1000, # in milliseconds
            n_intervals=0
        )
])
@app.callback(Output('Memory_pie_chart', 'figure'),
              Input('interval-component_files', 'n_intervals'))
def update_graph_live_memory(_):
    """ MEMORY CHART """
    time.sleep(0)
    memorylist = functions.get_memory(client)
    memorydata = {
        'Memory_Type': ['Total', 'Used', 'Free', 'Shared', 'Buff/Cache', 'Available'],
        'Memory': memorylist
    }
    dataframe = pd.DataFrame(memorydata)
    memory_graph = px.bar(dataframe, x="Memory_Type", y="Memory",
            color="Memory_Type", title="Usage of the memory of the remote server", barmode='stack')
    memory_graph.update_layout(xaxis_title='Name')
    return memory_graph

@app.callback(Output('File_size_graph', 'figure'),
              Input('interval-component_memory', 'n_intervals'))
def update_graph_live_file_size(_):
    """ FILES SIZE CHART """
    time.sleep(2)
    list_files = []
    list_size = []
    list_files, list_size = functions.get_biggest_files(client)
    sizedata = go.Bar(x=list_size, y=list_files)
    return go.Figure(data=sizedata)


@app.callback(Output('Pie_process_chart', 'figure'),
              Input('interval-component_process', 'n_intervals'))
def update_graph_live_process(_):
    """ PROCESSES CHART """
    time.sleep(4)
    processlist = functions.get_process_infos(client)
    process_labels = []
    process_values = []
    for process in processlist:
        process_labels.append(process.command)
        process_values.append(1)  # process.cpu
    return go.Figure(data=[go.Pie(labels=process_labels, values=process_values,
                                 title="Pie chart representing cpu usage by processes")])

@app.callback(Output('Logs_graph', 'figure'),
              Input('interval-component_logs', 'n_intervals'))
def update_graph_live_logs(_):
    """ LOGS CHART """
    time.sleep(6)
    logs = functions.get_access_logs(client)
    memory_labels = []
    memory_values = []
    for log in logs:
        memory_labels.append(log.name)
        memory_values.append(log.numberOfSearchs)
    return go.Figure(data=[go.Pie(labels=memory_labels, values=memory_values,
                                 title="Pie chart representing logs access")])

@app.callback(Output('Error_logs_graph', 'figure'),
              Input('interval-component_error_logs', 'n_intervals'))
def update_graph_live_error_logs(_):
    """ ERROR LOGS CHART """
    time.sleep(6)
    logs = functions.get_access_logs(client)
    memory_labels = []
    memory_values = []
    for log in logs:
        memory_labels.append(log.name)
        memory_values.append(log.numberOfSearchs)
    return go.Figure(data=[go.Pie(labels=memory_labels, values=memory_values,
                                 title="Pie chart representing logs access")])

if __name__ == '__main__':
    app.run_server(debug=True)
