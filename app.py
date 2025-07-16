import dash
from dash import dcc, html, dash_table, Input, Output
import pandas as pd

# Carregando o DataFrame
# Certifique-se de que 'controle_custos.xlsx' está no mesmo diretório do seu app.py
try:
    df = pd.read_excel('controle_custos.xlsx', sheet_name='Custos Das Casas')
    df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y', errors='coerce')
    # Remover linhas onde a data é NaT (Not a Time) após a conversão
    df.dropna(subset=['Data'], inplace=True)
except FileNotFoundError:
    print("Erro: O arquivo 'controle_custos.xlsx' não foi encontrado. Por favor, certifique-se de que ele está no mesmo diretório do script.")
    # Criar um DataFrame vazio para evitar erros no restante do código
    df = pd.DataFrame(columns=['Data', 'Categoria', 'Valor (R$)'])
except Exception as e:
    print(f"Erro ao carregar ou processar o arquivo Excel: {e}")
    df = pd.DataFrame(columns=['Data', 'Categoria', 'Valor (R$)'])


# Inicializando o app
app = dash.Dash(__name__)

# Obter opções únicas para o dropdown de categorias, se o DataFrame não estiver vazio
categorias_unicas = df['Categoria'].unique() if not df.empty else []

# Layout com duas linhas (gráfico em cima, tabela embaixo)
app.layout = html.Div([
    html.H1("Casa Geminada - Controle de Custos", style={'textAlign': 'center', 'color': '#333'}),

    # Linha de Filtros
    html.Div([
        html.H3("Filtros:", style={'margin-bottom': '10px'}),
        html.Div([
            html.Label("Selecionar Categoria:", style={'margin-right': '10px'}),
            dcc.Dropdown(
                id='categoria-dropdown',
                options=[{'label': cat, 'value': cat} for cat in categorias_unicas],
                placeholder="Selecione uma categoria",
                style={'width': '200px', 'display': 'inline-block', 'verticalAlign': 'middle'}
            ),
            html.Label("Filtrar por Data:", style={'margin-left': '20px', 'margin-right': '10px'}),
            dcc.DatePickerRange(
                id='date-picker',
                start_date_placeholder_text="Data Inicial",
                end_date_placeholder_text="Data Final",
                display_format='DD/MM/YYYY',
                style={'display': 'inline-block', 'verticalAlign': 'middle'}
            )
        ], style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center', 'margin-bottom': '20px'})
    ], style={'padding': '20px', 'borderBottom': '1px solid #eee', 'backgroundColor': '#f9f9f9'}),

    # Linha 1: Gráfico
    html.Div([
        html.H3("Gráfico de Custos por Categoria:", style={'textAlign': 'center'}),
        dcc.Graph(id='custo-grafico')
    ], style={'padding': '20px', 'backgroundColor': '#fff', 'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'margin': '20px 0'}),

    # Linha 2: Tabela
    html.Div([
        html.H3("Tabela de Custos", style={'textAlign': 'center'}),
        dash_table.DataTable(
            id='tabela-custos',
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns],
            page_size=10,
            style_table={'overflowX': 'auto', 'border': '1px solid #ddd', 'borderRadius': '8px'},
            style_cell={'textAlign': 'left', 'padding': '12px', 'borderBottom': '1px solid #eee'},
            style_header={
                'backgroundColor': '#007bff',
                'color': 'white',
                'fontWeight': 'bold',
                'textAlign': 'center'
            },
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(248, 248, 248)'
                }
            ]
        )
    ], style={'padding': '20px', 'backgroundColor': '#fff', 'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'margin': '20px 0'})
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

    # Agrupar e criar o gráfico
    if not filtered_df.empty:
        agrupado = filtered_df.groupby('Categoria')['Valor (R$)'].sum().reset_index()
        titulo = f'Total de Custo para {categoria}' if categoria else 'Total de Custo por Categoria'
        fig = {
            'data': [{
                'x': agrupado['Categoria'],
                'y': agrupado['Valor (R$)'],
                'type': 'bar',
                'marker': {'color': '#1f77b4'}, # Cor mais vibrante
                'name': 'Custo'
            }],
            'layout': {
                'title': titulo,
                'xaxis': {'title': 'Categoria'},
                'yaxis': {'title': 'Valor Total (R$)'},
                'plot_bgcolor': '#f0f0f0', # Cor de fundo do plot
                'paper_bgcolor': '#fff', # Cor de fundo do papel
                'margin': {'l': 40, 'r': 40, 't': 80, 'b': 40}
            }
        }
    else:
        # Retorna um gráfico vazio ou uma mensagem se não houver dados
        fig = {
            'data': [],
            'layout': {
                'title': 'Nenhum dado para exibir com os filtros selecionados',
                'xaxis': {'visible': False},
                'yaxis': {'visible': False}
            }
        }
    return fig

# ESSENCIAL para o Gunicorn: Expor a instância do servidor
server = app.server

# Rodar o servidor (apenas para desenvolvimento local)
#if __name__ == '__main__':
#   app.run_server(debug=True, port=8050) # Use app.run_server para Dash
