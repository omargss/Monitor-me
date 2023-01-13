import json
import time
import dash
from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
import client_class

app = Dash(__name__)

with open('config.json',"r",encoding="utf-8") as f:
    data = json.load(f)

machines=data['machines']

output = []

output.append(dcc.Location(id='url',refresh=False))

output.append(
     html.Div([
        html.Label('Hostname: '),
        dcc.Input(id='hostname', type='text'),
        html.Label('Port: '),
        dcc.Input(id='port', type='text'),
        html.Label('Username: '),
        dcc.Input(id='username', type='text'),
        html.Label('Password: '),
        dcc.Input(id='password', type='password'),
        html.Button('Save', id='saveBtn'),
    ])
)


for machine in machines:
    try:
        client = client_class.Client(machine["hostname"],machine["port"],machine["username"],machine["password"])
        client.connection()
        output.append(html.Div(machine["hostname"]+"    Online"))
    except Exception as e:
        output.append(html.Div(machine["hostname"]+"    Offline"))
output.append(html.Ul(id="new_machines"))

app.layout = html.Div(children=output)

@app.callback(
    [Output('new_machines','children')],
    [Input('saveBtn','n_clicks')],
    [
        State('hostname','value'),
        State('port','value'),
        State('username','value'),
        State('password','value'),
    ]
)
def update(n_click, input_hostname,input_port,input_username,input_password):
    """ UPDATE JSON """
    if n_click:
        with open("config.json", "r",encoding="utf-8") as file:
            config_json = json.load(file)
            config_json["machines"].append({
                "hostname": input_hostname,
                "port": input_port,
                "username": input_username,
                "password": input_password
        })

        with open("config.json", "w",encoding="utf-8") as file:
            json.dump(config_json, file, indent=4)
        time.sleep(0.5)
        with open('config.json',"r",encoding="utf-8") as f:
            data_callback = json.load(f)
        machines_callback=data_callback['machines']
        list_li = []
        for machine_callback in machines_callback:
            try:
                client = client_class.Client(machine_callback["hostname"],machine_callback["port"],machine_callback["username"],machine_callback["password"])
                client.connection()
                list_li.append(html.Li(machine_callback["hostname"]+"    Online"))
            except Exception as _:
                list_li.append(html.Li(machine_callback["hostname"]+"    Offline"))
        print(list_li)
        return list_li

if __name__ == '__main__':
    app.run_server(debug=True)