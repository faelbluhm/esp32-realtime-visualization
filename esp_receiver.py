import socket

def esp_data_stream(host='192.168.0.2', port=1234):
    s = socket.socket()
    s.connect((host, port))
    try:
        while True:
            data = s.recv(32)
            if data:
                yield data.decode().strip()
    finally:
        s.close()
