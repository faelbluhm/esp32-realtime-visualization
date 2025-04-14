# ESP32 Real-time Signal Visualization

A system for real-time visualization of signals from an ESP32 microcontroller using a Python backend and interactive web dashboard.

## Overview

This project implements a complete data pipeline to capture, process, and visualize signals from an ESP32 microcontroller in real-time:

1. **ESP32 (Signal Generation)**: Generates a sine wave signal with Gaussian noise and sends it via TCP Socket
2. **Python API (FastAPI)**: Acts as a bridge, receiving data from the ESP32 and forwarding it to clients via WebSockets
3. **Web Dashboard (Dash/Plotly)**: Visualizes the incoming data stream in an interactive graph

## Project Structure

```
├── esp32/
│   └── main.py                # MicroPython code for ESP32
├── server/
│   └── api.py                 # FastAPI server with WebSocket endpoint
├── frontend/
│   └── frontend.py            # Dash/Plotly web dashboard
├── README.md
└── LICENSE
```

## Installation

### Requirements

- Python 3.7+
- ESP32 with MicroPython firmware
- Required Python packages:
  ```
  fastapi
  uvicorn
  dash
  plotly
  websockets
  ```

### Installation Steps

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/esp32-realtime-visualization.git
   cd esp32-realtime-visualization
   ```

2. Install required Python packages:
   ```bash
   pip install fastapi uvicorn dash plotly websockets
   ```

3. Upload the `esp32/main.py` file to your ESP32 device (using tools like ampy, rshell, or Thonny IDE)

## Usage

### 1. ESP32 Setup

1. Modify the ESP32 code in `esp32/main.py` to match your WiFi credentials:
   ```python
   wifi.connect('your_wifi_ssid', 'your_wifi_password')
   ```

2. Run the code on the ESP32. It will:
   - Connect to WiFi
   - Start a TCP server on port 1234
   - Generate and send a sine wave signal with noise

### 2. Start the Backend API

Run the FastAPI server:
```bash
cd server
python api.py
```

The server will:
- Connect to the ESP32 via TCP socket on port 1234
- Process incoming data
- Expose a WebSocket endpoint at `ws://localhost:8001/ws`

### 3. Launch the Web Dashboard

Start the Dash frontend:
```bash
cd frontend
python frontend.py
```

Access the dashboard at: http://localhost:8050

## How It Works

1. The ESP32 generates a sine wave with noise at 50Hz and sends it through a TCP socket
2. The FastAPI server receives this data, processes it, and forwards it through a WebSocket connection
3. The Dash frontend connects to the WebSocket, receives the data, and updates the graph in real-time

## Fallback Mode

If the API can't connect to the ESP32, it automatically enters a simulation mode, generating synthetic data that mimics the ESP32's output.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/) for the high-performance API framework
- [Dash/Plotly](https://dash.plotly.com/) for the interactive visualization
- [MicroPython](https://micropython.org/) for ESP32 programming
