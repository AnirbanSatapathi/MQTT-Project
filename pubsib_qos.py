import paho.mqtt.client as mqtt
import time

BROKER = "localhost"
PORT = 1883
TOPIC = "qos/test"

# --- Subscriber setup ---
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Subscriber connected to broker")
        # Subscribe with all QoS levels
        for qos in [0, 1, 2]:
            client.subscribe(TOPIC, qos=qos)
            print(f"Subscribed to {TOPIC} with QoS {qos}")
    else:
        print("Connection failed with code", rc)

def on_message(client, userdata, msg):
    print(f"[Subscriber] Received: {msg.payload.decode()} "
          f"on topic {msg.topic} with QoS {msg.qos}")

sub_client = mqtt.Client(
    client_id="subscriber_qos",
    protocol=mqtt.MQTTv311,
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
)
sub_client.on_connect = on_connect
sub_client.on_message = on_message
sub_client.connect(BROKER, PORT, keepalive=60)
sub_client.loop_start()

time.sleep(3)  # allow subscriber to connect

# --- Publisher setup ---
pub_client = mqtt.Client(
    client_id="publisher_qos",
    protocol=mqtt.MQTTv311,
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
)
pub_client.connect(BROKER, PORT, keepalive=60)
pub_client.loop_start()

# --- Continuous publishing ---
count = 0
try:
    while True:
        for qos in [0, 1, 2]:
            message = f"Message {count} with QoS {qos}"
            result = pub_client.publish(TOPIC, message, qos=qos)
            status = result[0]
            if status == 0:
                print(f"[Publisher] Sent: {message}")
            else:
                print(f"[Publisher] Failed to send: {message}")
        count += 1
        time.sleep(2)  # send every 2 seconds
except KeyboardInterrupt:
    print("Stopping...")

sub_client.loop_stop()
sub_client.disconnect()
pub_client.loop_stop()
pub_client.disconnect()
