import network
import socket
import time
import math
import random

# Função para ruído gaussiano
def gauss(mu=0, sigma=1):
    u1 = random.random()
    u2 = random.random()
    z0 = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
    return z0 * sigma + mu

# Conectar ao Wi-Fi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect('brisa-3809634', '0nxygivh')

while not wifi.isconnected():
    pass

print('Conectado ao Wi-Fi. IP:', wifi.ifconfig()[0])

# Criar socket servidor
addr = socket.getaddrinfo('0.0.0.0', 1234)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
print("Aguardando conexão...")

conn, addr = s.accept()
print('Conectado a', addr)

# Geração do sinal
f = 1
A = 1
Fs = 20
t = 0

while True:
    noise = gauss(0, 0.1)
    value = A * math.cos(2 * math.pi * f * t) + noise
    conn.send((str(value) + "\n").encode())  # Enviar como bytes
    t += 1 / Fs
    time.sleep(1 / Fs)
