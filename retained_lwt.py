import paho.mqtt.client as mqtt
import time

BROKER = "localhost"
PORT = 1883

TOPIC_STATE = "devices/device1/state"
TOPIC_STATUS = "devices/device1/status"

def on_connect(client, userdata, flags, rc, properties=None):
    if rc ==0:
        print("Subscriber connected to broker")
        client.subscribe([(TOPIC_STATE, 1),(TOPIC_STATUS,1)])
    else:
        print("Connection failed with code", rc)

def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode()} on topic {msg.topic} (retained={msg.retain})")

sub = mqtt.Client(
    client_id="subscriber_retained",
    protocol=mqtt.MQTTv311,
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
)
sub.on_connect = on_connect
sub.on_message = on_message
sub.connect(BROKER, PORT, keepalive=60)
sub.loop_start()

time.sleep(3)

#Publisher with LWT
pub = mqtt.Client(
    client_id="publisher_retained",
    protocol=mqtt.MQTTv311,
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
)
pub.will_set(TOPIC_STATUS, payload="offline", qos=1, retain=True)
pub.connect(BROKER, PORT, keepalive=60)

pub.publish(TOPIC_STATE, payload="online", qos=1, retain=True)
pub.publish(TOPIC_STATE," device1 is active", qos=1, retain=True)
time.sleep(3)

print("simulating disconnection...")
pub.loop_stop()
pub._sock.close()  # Simulate disconnection by closing the socket
time.sleep(5)  # Wait to ensure LWT is processed

sub.loop_stop()
sub.disconnect()