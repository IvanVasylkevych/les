import logging
import time
import json
import paho.mqtt.client as mqtt


from config import (
    MQTT_TOPIC,
    MQTT_BROKER_HOST,
    MQTT_BROKER_PORT,
)



# MQTT
client = mqtt.Client()


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logging.info("Connected to MQTT broker")
        client.subscribe(MQTT_TOPIC)
    else:
        logging.info(f"Failed to connect to MQTT broker with code: {rc}")


def publish(client, topic):
    processed_data = {"road_state": "bad", "agent_data":
        {
            "accelerometer": {"x": 1.0, "y": 12.0, "z": 4.0},
            "gps": {"latitude": 56.21, "longitude": 19.5641},
            "timestamp": "2024-03-15T14:34:20.236457"
        }
                      }
    json_string = json.dumps(processed_data)
    while True:
        client.publish(topic, payload=json_string)
        time.sleep(1)

# Connect
client.on_connect = on_connect
client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT)

# Start
client.loop_start()
publish(client=client, topic=MQTT_TOPIC)

