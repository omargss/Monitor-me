from dash import Dash, html
import dash

app = Dash(__name__, use_pages=True)

app.layout = html.Div([
	html.H1('Dash monitoring application'),
	dash.page_container
])

if __name__ == '__main__':
	app.run_server(host='0.0.0.0', port=8050, debug=False)
