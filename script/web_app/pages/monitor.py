""" Python web app """
# pylint: disable=pointless-string-statement
# pyling: disable=unused-argument

import time
import json
import dash
from dash import callback, html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import functions
import client_class

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
""" SERVER CONNECTION """
"""config = configparser.RawConfigParser()
config.read("../config.txt")
hostname = config['settings']['hostname']
port = config['settings']['port']
username = config['settings']['username']
password = config['settings']['password']"""


url=""
index=0

with open('config.json',"r",encoding="utf-8") as f:
    data = json.load(f)

machines=data['machines']

hostname=machines[index]['hostname']
port = machines[index]['port']
username = machines[index]['username']
password=machines[index]['password']


client = client_class.Client(hostname,port,username,password)

""" WEB DISPLAY """
COLOR1 ='#272643'
COLOR2 ='#2c698d'
COLOR3 ='#ffffff'

dash.register_page(__name__,path_template="/machine/<hostname_url>")


layout = html.Div(children=[
    dcc.Location(id='url', refresh=False),
    html.Div(id="p"),
    html.Br(),
    html.Br(),
    dcc.Loading(id="ls-loading-1",children=[html.Div(id="ls-loading-output-1"),
        dcc.Link("Go back home", href="/")], type="default"),
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
        id='interval-component',
        interval=10*1000,  # in milliseconds
        n_intervals=0
    )
])

""" CALLBACKS """

@callback(Output("ls-loading-output-1",'children'), [Input('url', 'pathname')])
def loading(pathname):
    """ LOADING STATE"""
    if pathname != '/':
        url = pathname
        index = int(url.removeprefix("/machine/"))
        hostname=machines[index]['hostname']
        port = machines[index]['port']
        username = machines[index]['username']
        password=machines[index]['password']


        client = client_class.Client(hostname,port,username,password)

        client.connection()
        time.sleep(1)
        return hostname
    else :
        return dash.no_update


@callback(Output('Memory_pie_chart', 'figure'),
                    Output('File_size_graph', 'figure'),
                    Output('Pie_process_chart', 'figure'),
                    Output('Logs_graph', 'figure'),
                    Output('Error_logs_graph', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph_live(_):
    """ MEMORY CHART """
    memorylist = functions.get_memory(client)
    memorydata = {
        'Memory_Type': ['Total', 'Used', 'Free', 'Shared', 'Buff/Cache', 'Available'],
        'Memory': memorylist
    }
    dataframe = pd.DataFrame(memorydata)
    memory_graph = px.bar(dataframe, x="Memory_Type", y="Memory",
                          color="Memory_Type", title="Usage of the memory of the remote server", barmode='stack')
    memory_graph.update_layout(xaxis_title='Error type', plot_bgcolor=COLOR1,paper_bgcolor=COLOR2,font={"color":COLOR3})
    """ FILES SIZE CHART """
    list_files = []
    list_size = []
    list_files, list_size = functions.get_biggest_files(client)
    sizedata = go.Bar(x=list_size, y=list_files)
    file_size_chart = go.Figure(data=sizedata).update_layout(plot_bgcolor=COLOR1,paper_bgcolor=COLOR2,font={"color":COLOR3})
    """ PROCESSES CHART """
    processlist = functions.get_process_infos(client)
    process_labels = []
    process_values = []
    for process in processlist:
        process_labels.append(process.command)
        process_values.append(1)  # process.cpu
    process_chart = go.Figure(data=[go.Pie(labels=process_labels, values=process_values,
                                  title="Pie chart representing cpu usage by processes")]).update_layout(plot_bgcolor=COLOR1,paper_bgcolor=COLOR2,font={"color":COLOR3})
    """ LOGS CHART """
    logs = functions.get_access_logs(client)
    memory_labels = []
    memory_values = []
    for log in logs:
        memory_labels.append(log.name)
        memory_values.append(log.numberOfSearchs)
    logs_chart = go.Figure(data=[go.Pie(labels=memory_labels, values=memory_values,
        title="Pie chart representing most viewed pages")]).update_layout(plot_bgcolor=COLOR1,paper_bgcolor=COLOR2,font={"color":COLOR3})
    """ ERROR LOGS CHART """
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
    return memory_graph, file_size_chart, process_chart, logs_chart, error_graph


@callback(
    Output("Errors", "children"),
    Input("Error_logs_graph", "clickData"),
)
def fig_click(click_data):
    """ Function that handles clicks"""
    if not click_data:
        raise dash.exceptions.PreventUpdate
    warn_list, emerg_list, alert_list, crit_list, error_list, info_list, notice_list, debug_list = functions.get_error_logs(
        client)
    temp = []
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
