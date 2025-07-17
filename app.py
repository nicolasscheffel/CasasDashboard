import dash
from dash import html

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Olá, mundo!"),
    html.P("Este é um exemplo básico de Dash para testar no Render.")
])

server = app.server  # necessário para o Render

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8050))  # Render define a variável PORT
    app.run(host='0.0.0.0', port=port, debug=True)