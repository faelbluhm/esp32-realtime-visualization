import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import threading
import asyncio
import websockets
from collections import deque
import time

# Buffer circular com tamanho máximo para armazenar os últimos N pontos
data_buffer = deque(maxlen=200)
time_buffer = deque(maxlen=200)
start_time = time.time()

# Função para receber dados via WebSocket
async def websocket_receiver():
    # Atualizando a porta para 8001
    uri = "ws://localhost:8001/ws"
    while True:
        try:
            async with websockets.connect(uri) as websocket:
                print("Conectado ao servidor WebSocket")
                while True:
                    msg = await websocket.recv()
                    current_time = time.time() - start_time
                    if msg == "error":
                        print("Erro na conexão com ESP32")
                        continue
                    try:
                        value = float(msg)
                        data_buffer.append(value)
                        time_buffer.append(current_time)
                        #print(f"Recebido: {value}")
                    except ValueError:
                        print(f"Valor inválido recebido: {msg}")
        except websockets.exceptions.ConnectionClosedError:
            print("Conexão WebSocket fechada, reconectando...")
            await asyncio.sleep(1)
        except Exception as e:
            print(f"Erro no WebSocket: {e}")
            await asyncio.sleep(1)

# Thread para executar o loop assíncrono
def websocket_thread():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(websocket_receiver())

# Inicia a thread do WebSocket
threading.Thread(target=websocket_thread, daemon=True).start()

# Configuração do app Dash
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H2("Sinal em Tempo Real do ESP32"),
    dcc.Graph(id='live-graph'),
    dcc.Interval(id='interval-component', interval=200, n_intervals=0)

])

# Callback para atualizar o gráfico
@app.callback(
    Output('live-graph', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_graph(n):
    # Cria uma figura com os dados do buffer
    fig = go.Figure()

    if len(data_buffer) > 0:
        fig.add_trace(go.Scatter(
            x=list(time_buffer),
            y=list(data_buffer),
            mode='lines',
            name='Sinal'
        ))

        # Ajusta o layout do gráfico
        fig.update_layout(
            title='Sinal do ESP32',
            xaxis=dict(title='Tempo (s)'),
            yaxis=dict(title='Amplitude'),
            height=600
        )

    return fig

if __name__ == '__main__':
    app.run(debug=False, port=8050)
