""" Python web app """
# pylint: disable=pointless-string-statement
# pyling: disable=unused-argument
import configparser
import time
import dash
from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import functions
import client_class
import json

app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
""" SERVER CONNECTION """
"""config = configparser.RawConfigParser()
config.read("../config.txt")
hostname = config['settings']['hostname']
port = config['settings']['port']
username = config['settings']['username']
password = config['settings']['password']"""

with open('config.json',"r",encoding="utf-8") as f:
    data = json.load(f)

machines=data['machines']
hostname=machines[0]['hostname']
port = machines[0]['port']
username = machines[0]['username']
password=machines[0]['password']


client = client_class.Client(hostname,port,username,password)

client.connection()

""" WEB DISPLAY """
COLOR1 ='#272643'
COLOR2 ='#2c698d'
COLOR3 ='#ffffff'
app.layout = html.Div(children=[
    dcc.Location(id='url', refresh=False),
    html.H1(children='Monitoring web application'),
    html.Div([
        html.Label('Hostname: '),
        dcc.Input(id='hostname', value=hostname, type='text'),
        html.Label('Port: '),
        dcc.Input(id='port', value=port, type='text'),
        html.Label('Username: '),
        dcc.Input(id='username', value=username, type='text'),
        html.Label('Password: '),
        dcc.Input(id='password', value=password, type='password'),
        html.Button('Connection', id='btnConnection'),
    ]),
    html.Br(),
    html.Br(),
    dcc.Loading(id="ls-loading-1",children=[html.Div(id="ls-loading-output-1")], type="default"),
    html.Div(id='Display', children=[
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
    html.Ul(id='Errors')
    ]),

    dcc.Interval(
        id='interval-component_memory',
        interval=20*1000,  # in milliseconds
        n_intervals=0
    ),
    dcc.Interval(
        id='interval-component_files',
        interval=100*1000,  # in milliseconds
        n_intervals=0
    ),
    dcc.Interval(
        id='interval-component_process',
        interval=20*1000,  # in milliseconds
        n_intervals=0
    ),
    dcc.Interval(
        id='interval-component_logs',
        interval=20*1000,  # in milliseconds
        n_intervals=0
    ),
    dcc.Interval(
        id='interval-component_error_logs',
        interval=60*1000,  # in milliseconds
        n_intervals=0
    ),
    dcc.Interval(
        id='interval-loading',
        interval=100,  # in milliseconds
        n_intervals=0
    ),
])
""" CALLBACKS """

@app.callback(Output("ls-loading-output-1",'children'), [Input('url', 'pathname')])
def loading(_):
    """ LOADING STATE"""
    time.sleep(20)
    return ''

@app.callback(
    [Output('hidden-div','children')],
    [Input('saveBtn','n_clicks')],
    [
        State('hostname','value'),
        State('port','value'),
        State('username','value'),
        State('password','value')
    ]
)
def update_config_JSON(_):
    with open("config.json", "r",encoding="utf-8") as file:
        configJSON = json.load(file)
        configJSON["machines"].append({
            "hostname": "test@tse",
            "port": 22000,
            "username": "cyril",
            "password": "mdp"
    })

    # Enregistrer les données modifiées dans le fichier JSON

    with open("config.json", "w") as f:
        json.dump(data, f, indent=4)

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
    memory_graph.update_layout(xaxis_title='Error type', plot_bgcolor=COLOR1,paper_bgcolor=COLOR2,font={"color":COLOR3})
    return memory_graph


@app.callback(Output('File_size_graph', 'figure'),
              Input('interval-component_memory', 'n_intervals'))
def update_graph_live_file_size(_):
    """ FILES SIZE CHART """
    time.sleep(4)
    list_files = []
    list_size = []
    list_files, list_size = functions.get_biggest_files(client)
    sizedata = go.Bar(x=list_size, y=list_files)
    return go.Figure(data=sizedata).update_layout(plot_bgcolor=COLOR1,paper_bgcolor=COLOR2,font={"color":COLOR3})


@app.callback(Output('Pie_process_chart', 'figure'),
              Input('interval-component_process', 'n_intervals'))
def update_graph_live_process(_):
    """ PROCESSES CHART """
    time.sleep(8)
    processlist = functions.get_process_infos(client)
    process_labels = []
    process_values = []
    for process in processlist:
        process_labels.append(process.command)
        process_values.append(1)  # process.cpu
    return go.Figure(data=[go.Pie(labels=process_labels, values=process_values,
                                  title="Pie chart representing cpu usage by processes")]).update_layout(plot_bgcolor=COLOR1,paper_bgcolor=COLOR2,font={"color":COLOR3})


@app.callback(Output('Logs_graph', 'figure'),
              Input('interval-component_logs', 'n_intervals'))
def update_graph_live_logs(_):
    """ LOGS CHART """
    time.sleep(12)
    logs = functions.get_access_logs(client)
    memory_labels = []
    memory_values = []
    for log in logs:
        memory_labels.append(log.name)
        memory_values.append(log.numberOfSearchs)
    return go.Figure(data=[go.Pie(labels=memory_labels, values=memory_values,
        title="Pie chart representing most viewed pages")]).update_layout(plot_bgcolor=COLOR1,paper_bgcolor=COLOR2,font={"color":COLOR3})


@app.callback(Output('Error_logs_graph', 'figure'),
              Input('interval-component_error_logs', 'n_intervals'))
def update_graph_live_error_logs(_):
    """ ERROR LOGS CHART """
    time.sleep(16)
    warn_list, emerg_list, alert_list, crit_list, error_list, info_list, notice_list, debug_list = functions.get_error_logs(
        client)
    error_data = {
        'Error_Type': ['Error', 'Warning', 'Critical', 'Emergency', 'Alert', 'Notice', 'Info', 'Debug'],
        'Errors': [len(error_list), len(warn_list), len(crit_list), len(emerg_list), len(alert_list), len(notice_list), len(info_list), len(debug_list)]
    }
    dataframe = pd.DataFrame(error_data)
    error_graph = px.bar(dataframe, x="Error_Type", y="Errors",
                         color="Error_Type", title="Log errors (click on error type to see details)", barmode='stack')
    error_graph.update_layout(xaxis_title='Error type', plot_bgcolor=COLOR1,paper_bgcolor=COLOR2,font={"color":COLOR3})
    return error_graph


@app.callback(
    Output("Errors", "children"),
    Input("Error_logs_graph", "clickData"),
)
def fig_click(click_data):
    """ Function that handles clicks"""
    if not click_data:
        raise dash.exceptions.PreventUpdate
    warn_list, emerg_list, alert_list, crit_list, error_list, info_list, notice_list, debug_list = functions.get_error_logs(
        client)
    temp = ''
    click = click_data["points"][0]["x"]
    if click == 'Error':
        temp = [html.Li(i) for i in error_list]
    elif click == 'Warning':
        temp = [html.Li(i) for i in warn_list]
    elif click == 'Critical':
        temp = [html.Li(i) for i in crit_list]
    elif click == 'Emergency':
        temp = [html.Li(i) for i in emerg_list]
    elif click == 'Alert':
        temp = [html.Li(i) for i in alert_list]
    elif click == 'Notice':
        temp = [html.Li(i) for i in notice_list]
    elif click == 'Info':
        temp = [html.Li(i) for i in info_list]
    elif click == 'Debug':
        temp = [html.Li(i) for i in debug_list]
    return temp


if __name__ == '__main__':
    app.run_server(debug=True)
