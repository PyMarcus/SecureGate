import json
import time

from apps.emulator.config.config import config
from apps.emulator.src.utils.log import Log
from apps.server.mqtt.mqtt_client import MQTTClient
from packages.constants.mqtt_topics import MQTTTopic


def on_activation_message(topic: str, payload: str):
    data = json.loads(payload)

    if data["action"] == "ACTIVATE":
        Log.info("Abrindo portão...")
        time.sleep(3)
        Log.success("Portão aberto com sucesso!")
        return

    if data["action"] == "DEACTIVATE":
        Log.info("Fechando portão...")
        time.sleep(3)
        Log.success("Portão fechado com sucesso!")
        return

    Log.danger("Ação inválida!")


def on_authorization_message(topic: str, payload: str):
    pass


def rfid_read():
    Log.break_()
    Log.info("Aguardando RFID...")
    rfid = input("=> ")
    if not rfid or len(rfid) != 8:
        Log.danger("Por favor, informe um RFID válido!")
        return None
    return rfid


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

    try:
        while True:
            Log.info("Aguardando RFID...")
            rfid = input("=> ")
            if not rfid or len(rfid) != 8:
                Log.danger("Por favor, informe um RFID válido!")
                continue

            print(rfid)

    except KeyboardInterrupt:
        mqtt.stop()
        Log.danger("Exiting...")
        exit(0)


_main()
