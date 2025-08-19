import paho.mqtt.client as mqtt
import time

BROKER = "localhost"
PORT = 1883
TOPIC = "test/topic"

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Connected to broker")
        client.subscribe(TOPIC)
    else:
        print("Connection failed with code", rc)

def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode()} on topic {msg.topic}")

# Subscriber client
sub_client = mqtt.Client(
    client_id="subscriber",
    protocol=mqtt.MQTTv311,
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
)
sub_client.on_connect = on_connect
sub_client.on_message = on_message
sub_client.connect(BROKER, PORT, keepalive=60)
sub_client.loop_start()

# Publisher client
pub_client = mqtt.Client(
    client_id="publisher",
    protocol=mqtt.MQTTv311,
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
)
pub_client.connect(BROKER, PORT, keepalive=60)

for i in range(11):
    message = f"Message {i+1}"
    pub_client.publish(TOPIC, message)
    print(f"Published: {message}")
    time.sleep(1)

time.sleep(2)
sub_client.loop_stop()
sub_client.disconnect()
pub_client.disconnect()
