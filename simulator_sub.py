import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
DEVICE_ID = "device1"

TOPIC_STATE = f"devices/{DEVICE_ID}/state"
TOPIC_STATUS = f"devices/{DEVICE_ID}/status"
TOPIC_SENSOR = f"devices/{DEVICE_ID}/sensor"

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("[New Subscriber] Connected to broker")
        # Subscribe to all device topics with QoS 1
        client.subscribe([
            (TOPIC_STATE, 1),
            (TOPIC_STATUS, 1),
            (TOPIC_SENSOR, 1)
        ])
    else:
        print("[New Subscriber] Connection failed with code", rc)

def on_message(client, userdata, msg):
    print(f"[New Subscriber] Received: {msg.payload.decode()} on {msg.topic} (retained={msg.retain}, QoS={msg.qos})")

client = mqtt.Client(
    client_id="new_subscriber",
    protocol=mqtt.MQTTv311,
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2
)
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, PORT, keepalive=60)
client.loop_forever()
