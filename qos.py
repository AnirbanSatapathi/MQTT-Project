import paho.mqtt.client as mqtt
import time

BROKER = "localhost"
PORT = 1883
TOPIC = "qos/test"

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Subscriber connected to broker")
        for qos in [0, 1, 2]:
            client.subscribe(TOPIC, qos=qos)
            print(f"Subscribed to {TOPIC} with QoS {qos}")
    else:
        print("Connection failed with code", rc)

def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode()} on topic {msg.topic} with QoS {msg.qos}")

# Subscriber client
sub_client = mqtt.Client(
    client_id="subscriber_qos",
    protocol=mqtt.MQTTv311,
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
)
sub_client.on_connect = on_connect
sub_client.on_message = on_message
sub_client.connect(BROKER, PORT, keepalive=60)
sub_client.loop_start()

time.sleep(5) # Allow time for connection and subscription

#publisher client
pub_client = mqtt.Client(
    client_id="publisher_qos",
    protocol=mqtt.MQTTv311,
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
)
pub_client.connect(BROKER, PORT, keepalive=60)

for qos in [0, 1, 2]:
    message = f"Message with QoS {qos}"
    result = pub_client.publish(TOPIC, message, qos=qos)
    status = result[0]
    if status == 0:
        print(f"Published: {message} with QoS {qos}")
    else:
        print(f"Failed to publish message with QoS {qos}")
    time.sleep(1)

time.sleep(3)
sub_client.loop_stop()
sub_client.disconnect()
pub_client.disconnect()