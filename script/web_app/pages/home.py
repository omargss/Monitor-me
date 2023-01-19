"""Home page of the app, here you can add, delete and choose a machine to monitor"""
import json
import time
import dash
from dash import html, dcc, callback
from dash.dependencies import Input, Output, State
import client_class

dash.register_page(__name__, path="/")

list_machine = []


layout = html.Div(children=[
    html.Div([
        html.Label('Hostname: '),
        dcc.Input(id='hostname', type='text'),
        html.Label('Port: '),
        dcc.Input(id='port', type='text'),
        html.Label('Username: '),
        dcc.Input(id='username', type='text'),
        html.Label('Password: '),
        dcc.Input(id='password', type='password'),
        html.Button('Save', id='saveBtn', n_clicks=0),
        html.Br(),
        html.Br(),
        html.Label('Delete machine'),
        dcc.Input(id='numMachine', type='number', min='0'),
        html.Button('Delete', id='deleteBtn', n_clicks=0)
    ]),
    html.Div(id="machine", children=[
        html.Ul(list_machine, id="new_machines")
    ])
])

@callback(
    [Output('new_machines', 'children')],
    [Input('saveBtn', 'n_clicks'),
     Input('deleteBtn', 'n_clicks')
    ],
    [
        State('hostname', 'value'),
        State('port', 'value'),
        State('username', 'value'),
        State('password', 'value'),
        State('numMachine', 'value')
    ]
)
def update(_, __ , input_hostname, input_port, input_username, input_password, num_machine):
    """ UPDATE JSON """
    ctx = dash.callback_context
    trigger = ctx.triggered[0]
    if trigger['prop_id'] == 'saveBtn.n_clicks':
        with open("config.json", "r", encoding="utf-8") as file:
            data_callback = json.load(file)
        data_callback["machines"].append({
            "hostname": input_hostname,
            "port": input_port,
            "username": input_username,
            "password": input_password
        })

        with open("config.json", "w", encoding="utf-8") as file:
            json.dump(data_callback, file, indent=4)
        time.sleep(1)
    elif trigger['prop_id'] == 'deleteBtn.n_clicks':
        with open('config.json', 'r', encoding='utf-8') as json_file:
            data_callback = json.load(json_file)
        del data_callback['machines'][num_machine]
        with open('config.json', 'w', encoding='utf-8') as json_file:
            json.dump(data_callback, json_file, indent=4)

    with open('config.json', "r", encoding="utf-8") as file:
        data_callback = json.load(file)
    machines_callback = data_callback['machines']
    list_li = []
    i = 0
    for machine_callback in machines_callback:
        try:
            client_callback = client_class.Client(
                machine_callback["hostname"], machine_callback["port"], machine_callback["username"]
                ,machine_callback["password"])
            client_callback.connection()
            list_li.append(html.Li(children=[html.P(str(i)+".  "), dcc.Link(
                machine_callback["hostname"]+":    Online", className="online"
                , href="machine/"+str(i))]))
        except Exception as _:
            list_li.append(html.Li(children=[html.P(str(
                i)+".  "), html.P(machine_callback["hostname"]+":    Offline",
                className="offline")]))
        i = i+1
    return [list_li]
