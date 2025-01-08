# MQTT Brokers and Client Simulation Project

This project demonstrates setting up multiple MQTT brokers using Docker containers and simulating multiple MQTT clients with Python. The setup includes two MQTT brokers and a Python script for simulating multiple clients publishing sensor-like data.

## Prerequisites

- Docker
- Python 3.x
- pip (Python package manager)
- Docker Network (mqtt_network)

## Installation

1. Install the required Python package:
```bash
pip install paho-mqtt
```

2. Create a Docker network for the MQTT brokers:
```bash
docker network create mqtt_network
```

## Project Structure

```
mqtt-project/
├── config/
│   ├── broker1.conf
│   └── broker2.conf
├── Dockerfile
├── mqtt_simulation.py
└── README.md
```

## Broker Configuration

### Broker Configuration Files

Create two configuration files for the MQTT brokers with the following content:

#### broker1.conf and broker2.conf
```conf
persistence true
persistence_location /mosquitto/data/
log_dest file /mosquitto/log/mosquitto.log
listener 1883
allow_anonymous true
```

### Dockerfile

The Dockerfile uses the official Eclipse Mosquitto image and sets up the broker configuration:

```dockerfile
FROM eclipse-mosquitto
COPY broker.conf /mosquitto/config/
EXPOSE 1883
CMD ["mosquitto", "-c", "/mosquitto/config/broker.conf"]
```

## Running the Brokers

Start both MQTT brokers using Docker:

```bash
# Start Broker 1
docker run -d --name mqtt_broker1 \
  --network mqtt_network \
  -p 1884:1883 \
  -v $(pwd)/config/broker1.conf:/mosquitto/config/mosquitto.conf \
  eclipse-mosquitto

# Start Broker 2
docker run -d --name mqtt_broker2 \
  --network mqtt_network \
  -p 1885:1883 \
  -v $(pwd)/config/broker2.conf:/mosquitto/config/mosquitto.conf \
  eclipse-mosquitto
```

## Testing the Brokers

You can test the brokers using the Mosquitto command-line clients:

```bash
# Subscribe to Broker 1
mosquitto_sub -h localhost -p 1884 -t test/topic

# Publish to Broker 1
mosquitto_pub -h localhost -p 1884 -t test/topic -m "Hello Broker 1"

# Subscribe to Broker 2
mosquitto_sub -h localhost -p 1885 -t test/topic

# Publish to Broker 2
mosquitto_pub -h localhost -p 1885 -t test/topic -m "Hello Broker 2"
```

## Client Simulation

The `mqtt_simulation.py` script simulates multiple MQTT clients publishing sensor-like data to the broker.

### Features

- Simulates up to n number of concurrent clients
- Each client publishes JSON payloads containing:
  - Client ID
  - Temperature (15-45°C)
  - Humidity (20-99%)
  - Light sensor reading (1-1023)
- QoS level 1 messaging
- Retained messages
- Random publishing intervals (1-3 seconds)
- 60-second runtime per client
- Thread-based client simulation

### Running the Simulation

```bash
python mqtt_simulation.py
```

### Sample JSON Payload

```json
{
    "client_id": "client-1",
    "temp": 28,
    "hum": 65,
    "ldr": 512
}
```

## Configuration Parameters

The simulation script includes several configurable parameters:

- `BROKER`: MQTT broker hostname (default: "localhost")
- `PORT`: MQTT broker port (default: 1885)
- `TOPIC`: MQTT topic for publishing/subscribing (default: "test/topic")
- `NUM_CLIENTS`: Number of simulated clients (default: 15)
- `RUN_TIME`: Duration for each client to run in seconds (default: 60)

## Troubleshooting

1. If the brokers fail to start, check:
   - Port availability (1884 and 1885)
   - Docker network existence
   - Configuration file paths

2. If clients fail to connect:
   - Verify broker status
   - Check network connectivity
   - Confirm port mappings
