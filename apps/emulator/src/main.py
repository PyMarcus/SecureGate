import time

from apps.emulator.config.config import config
from apps.emulator.src.utils.log import Log
from apps.server.mqtt.mqtt_client import MQTTClient
from packages.constants.mqtt_topics import MQTTTopic


def on_activation_message(topic: str, payload: str):
    print(topic, payload)


def on_authorization_message(topic: str, payload: str):
    pass


def _main():
    mqtt_config = config.get("mqtt")
    host, port = mqtt_config.get("host"), mqtt_config.get("port")

    Log.info(f"Starting MQTT client on {host}:{port}...")
    time.sleep(5)

    mqtt = MQTTClient(host, port)
    Log.success("MQTT client started successfully!")

    mqtt.subscribe(MQTTTopic.ACTIVATION.value, on_activation_message)
    mqtt.subscribe(MQTTTopic.AUTHORIZATION.value, on_authorization_message)

    mqtt.listen()


_main()
