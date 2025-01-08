import time
import random
import json
import paho.mqtt.client as mqtt
import threading

# MQTT Broker details
BROKER = "localhost"
PORT = 1885
TOPIC = "test/topic"
NUM_CLIENTS = 15
RUN_TIME = 60  # Time duration for each client to run in seconds

# Generate random values for the JSON payload
def generate_json_payload(client_id):
    temp = random.randint(15, 45)  # Temperature between 15 and 45
    hum = random.randint(20, 99)   # Humidity between 20 and 99
    ldr = random.randint(1, 1023)  # Light sensor reading between 1 and 1023

    # Create the payload dictionary including the client_id
    payload = {
        "client_id": f"client-{client_id}",
        "temp": temp,
        "hum": hum,
        "ldr": ldr
    }

    # Convert dictionary to JSON string
    return json.dumps(payload)

# Callback when a message is received
def on_message(client, userdata, message):
    print(f"Client {client._client_id.decode()} received message: {message.payload.decode()}")

# Callback when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    print(f"Client {client._client_id.decode()} connected with result code {rc}")
    client.subscribe(TOPIC)

# Function to simulate each MQTT client
def mqtt_client(client_id):
    client = mqtt.Client(client_id=f"client-{client_id}")

    # Set callbacks
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(BROKER, PORT, 60)
    client.loop_start()

    # Track start time
    start_time = time.time()
    while time.time() - start_time < RUN_TIME:
        message = generate_json_payload(client_id)  # Pass the client_id here
        print(f"Client {client_id} publishing: {message}")
        client.publish(TOPIC, message, qos=1, retain=True)  # QoS 1 with retained message
        time.sleep(random.uniform(1, 3))  # Publish at random intervals between 1-3 seconds

    # Stop client after the duration is reached
    client.loop_stop()
    client.disconnect()
    print(f"Client {client_id} has finished.")

# Function to simulate multiple clients
def start_clients():
    threads = []
    for client_id in range(1, NUM_CLIENTS + 1):
        thread = threading.Thread(target=mqtt_client, args=(client_id,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    start_clients()

