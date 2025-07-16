import dash
from dash import dcc, html, dash_table, Input, Output
import pandas as pd

# Carregando o DataFrame
df = pd.read_excel(r'C:\Users\BI\Downloads\Controle_Custos_Obra_Geminadas (1).xlsx', sheet_name='Custos Das Casas')
df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y', errors='coerce')

# Inicializando o app
app = dash.Dash(__name__)

# Layout com duas linhas (gráfico em cima, tabela embaixo)
app.layout = html.Div([
    html.H1("Casa Geminada - Controle de Custos"),

    # Linha 1: Gráfico
    html.Div([
        html.H3("Gráfico de Custos por Categoria:"),
        dcc.Graph(id='custo-grafico')
    ], style={'padding': '10px'}),

    # Linha 2: Tabela
    html.Div([
        html.H3("Tabela de Custos"),
        dash_table.DataTable(
            id='tabela-custos',
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns],
            page_size=10,
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'left'},
            style_header={'backgroundColor': '#e1e1e1', 'fontWeight': 'bold'}
        )
    ], style={'padding': '10px'})
])

# Callback para atualizar o gráfico com base nos filtros
@app.callback(
    Output('custo-grafico', 'figure'),
    Input('categoria-dropdown', 'value'),
    Input('date-picker', 'start_date'),
    Input('date-picker', 'end_date')
)
def update_graph(categoria, start_date, end_date):
    filtered_df = df.copy()

    # Filtro por data
    if start_date and end_date:
        filtered_df = filtered_df[(filtered_df['Data'] >= start_date) & (filtered_df['Data'] <= end_date)]

    # Filtro por categoria
    if categoria:
        filtered_df = filtered_df[filtered_df['Categoria'] == categoria]
        agrupado = filtered_df.groupby('Categoria')['Valor (R$)'].sum().reset_index()
        titulo = f'Total de Custo para {categoria}'
    else:
        agrupado = filtered_df.groupby('Categoria')['Valor (R$)'].sum().reset_index()
        titulo = 'Total de Custo por Categoria'

    # Criação do gráfico de barras
    fig = {
        'data': [{
            'x': agrupado['Categoria'],
            'y': agrupado['Valor (R$)'],
            'type': 'bar',
            'marker': {'color': '#0074D9'},
            'name': 'Custo'
        }],
        'layout': {
            'title': titulo,
            'xaxis': {'title': 'Categoria'},
            'yaxis': {'title': 'Valor Total (R$)'}
        }
    }
    return fig

# Rodar o servidor
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8050, debug=True)
