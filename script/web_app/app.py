# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
import paramiko;
import sys
import configparser 
import functions
from dash import Dash, html, dcc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

config = configparser.RawConfigParser()   
config.read("config.txt")
hostname = config['settings']['hostname']
port = config['settings']['port']
username = config['settings']['username']
password = config['settings']['password']

client = paramiko.SSHClient()
client.load_system_host_keys()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
client.connect(hostname = hostname, port=port, username=username, password=password)

memorylist = functions.get_memory(client)

data = {
        'Memory_Type': ['Total', 'Used', 'Free', 'Shared','Buff/Cache','Available'],
        'Memory': memorylist
        }
df = pd.DataFrame(data)
fig = px.bar(df, x="Memory_Type", y="Memory", color="Memory_Type", title="Usage of the memory of the remote server", barmode='stack')
fig.update_layout(xaxis_title='Name')


app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Graph(
        id='bar chart 1',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)