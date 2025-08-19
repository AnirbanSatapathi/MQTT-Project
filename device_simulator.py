import paho.mqtt.client as mqtt
import time
import random

BROKER = "localhost"
PORT = 1883
DEVICE_ID = "device1"

TOPIC_STATE = f"devices/{DEVICE_ID}/state"
TOPIC_STATUS = f"devices/{DEVICE_ID}/status"
TOPIC_SENSOR = f"devices/{DEVICE_ID}/sensor"

# ---------------- Subscriber Setup ----------------
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("[Subscriber] Connected to broker")
        # Subscribe to all device topics
        client.subscribe([
            (TOPIC_STATE, 1),
            (TOPIC_STATUS, 1),
            (TOPIC_SENSOR, 1)
        ])
    else:
        print("[Subscriber] Connection failed with code", rc)

def on_message(client, userdata, msg):
    print(f"[Subscriber] Received: {msg.payload.decode()} on {msg.topic} (retained={msg.retain})")

sub_client = mqtt.Client(
    client_id="subscriber_device",
    protocol=mqtt.MQTTv311,
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2
)
sub_client.on_connect = on_connect
sub_client.on_message = on_message
sub_client.connect(BROKER, PORT, keepalive=60)
sub_client.loop_start()

time.sleep(2)  # wait for subscriber connection

# ---------------- Publisher Setup ----------------
pub_client = mqtt.Client(
    client_id="publisher_device",
    protocol=mqtt.MQTTv311,
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2
)
# LWT: device offline
pub_client.will_set(TOPIC_STATUS, payload="offline", qos=1, retain=True)
pub_client.connect(BROKER, PORT, keepalive=60)
pub_client.loop_start()

# Set initial state and status
pub_client.publish(TOPIC_STATE, payload="online", qos=1, retain=True)
pub_client.publish(TOPIC_STATUS, payload="online", qos=1, retain=True)

# ---------------- Continuous Sensor Simulation ----------------
try:
    count = 0
    while True:
        # Simulate sensor readings
        temperature = round(random.uniform(20.0, 30.0), 2)
        humidity = round(random.uniform(30.0, 60.0), 2)
        sensor_data = f"T={temperature}C H={humidity}%"

        # Publish with QoS levels
        pub_client.publish(TOPIC_SENSOR, sensor_data, qos=1, retain=False)
        print(f"[Publisher] Sent: {sensor_data}")

        # Every 5 cycles, simulate network glitch
        if count % 5 == 0 and count != 0:
            print("\n--- Simulating abrupt disconnect ---")
            pub_client._sock.close()  # simulate network failure
            time.sleep(5)  # wait
            pub_client.reconnect()
            print("--- Reconnected ---\n")

        count += 1
        time.sleep(2)

except KeyboardInterrupt:
    print("Stopping simulator...")

sub_client.loop_stop()
sub_client.disconnect()
pub_client.loop_stop()
pub_client.disconnect()
