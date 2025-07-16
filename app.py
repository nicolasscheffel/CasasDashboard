import dash
from dash import html

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Olá, mundo!"),
    html.P("Este é um exemplo básico de Dash para testar no Render.")
])

server = app.server  # necessário para o Render

if __name__ == "__main__":
    app.run_server(debug=True)
