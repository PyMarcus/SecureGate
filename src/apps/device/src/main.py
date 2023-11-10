import json
import time

from apps.emulator.config.config import config
from apps.emulator.src.utils.log import Log
from apps.server.mqtt.mqtt_client import MQTTClient
from packages.constants.mqtt_topics import MQTTTopic


def on_activation_message(topic: str, payload: str):
    data = json.loads(payload)

    if data["device_id"] != config.get("id"):
        Log.danger("ID do dispositivo inválido!")
        return

    if data["action"] == "ACTIVATE":
        Log.warn("Abrindo portão...")
        time.sleep(3)
        Log.success("Portão aberto com sucesso!")
    elif data["action"] == "DEACTIVATE":
        Log.warn("Fechando portão...")
        time.sleep(3)
        Log.success("Portão fechado com sucesso!")
    else:
        Log.danger("Ação inválida!")


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
    mqtt.listen()

    try:
        while True:
            Log.info("Aguardando RFID...")
            rfid = input("=> ")
            if not rfid or len(rfid) != 8:
                Log.danger("Por favor, informe um RFID válido!")
                continue

            auth_payload = json.dumps(
                {
                    "device_id": config.get("id"),
                    "rfid": rfid,
                }
            )
            mqtt.publish(MQTTTopic.AUTHENTICATION.value, auth_payload)

    except KeyboardInterrupt:
        mqtt.stop()
        Log.danger("Exiting...")
        exit(0)


_main()
