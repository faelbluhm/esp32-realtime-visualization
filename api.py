from fastapi import FastAPI, WebSocket
import asyncio
import socket
import threading
import time
from queue import Queue
import math
import random

app = FastAPI()
data_queue = Queue()
last_received = None
connections_ok = False

# Função para receber dados do ESP32 e colocar na fila
def esp32_receiver():
    global connections_ok, last_received
    try:
        with socket.socket() as s:
            print("Tentando conectar ao ESP32...")
            s.connect(('192.168.0.2', 1234))
            print("Conectado ao ESP32!")
            connections_ok = True

            while True:
                data = s.recv(32)
                if not data:
                    print("Conexão com ESP32 encerrada")
                    break

                # Decodifica a linha que contém múltiplos valores
                try:
                    line = data.decode().strip()
                    # Removido o log que mostrava cada linha recebida

                    # Divide a linha em valores individuais
                    values = line.split()
                    for value in values:
                        # Verifica se é um número válido
                        float_value = float(value)
                        # Coloca na fila para enviar ao frontend
                        data_queue.put(value)

                    last_received = time.time()
                except ValueError as e:
                    print(f"Erro ao processar valor: {e}")
                except Exception as e:
                    print(f"Erro ao processar dados: {e}")
    except Exception as e:
        print(f"Erro ao conectar ao ESP32: {e}")
        connections_ok = False

    print("Thread de recepção ESP32 encerrada, iniciando modo de simulação")
    # Se não conseguir conectar, inicia modo de simulação
    generate_fake_data()

# Função para gerar dados simulados caso o ESP32 não esteja disponível
def generate_fake_data():
    print("Gerando dados simulados...")
    i = 0
    while True:
        # Gera um valor senoidal + ruído aleatório
        value = math.sin(i * 0.1) + random.uniform(-0.2, 0.2)
        data_queue.put(str(value))
        i += 1
        time.sleep(0.2)  # 5 Hz

# Inicia o thread para receber dados do ESP32
esp_thread = threading.Thread(target=esp32_receiver, daemon=True)
esp_thread.start()

# Endpoint WebSocket para enviar dados para o frontend
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("Cliente WebSocket conectado")

    # Informa o cliente sobre o status da conexão
    status = "ESP32 conectado" if connections_ok else "Usando dados simulados"
    await websocket.send_text(f"status:{status}")

    # Removido o contador e os logs de envio
    while True:
        # Se tiver dados na fila, envia para o cliente WebSocket
        if not data_queue.empty():
            value = data_queue.get()
            await websocket.send_text(value)
        else:
            # Espera um pouco se não houver dados
            await asyncio.sleep(0.05)

if __name__ == "__main__":
    import uvicorn
    print("Iniciando servidor FastAPI na porta 8001...")
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="warning")  # Alterado para warning para reduzir logs
