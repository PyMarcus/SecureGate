import json
import time

from src.apps.device.config.config import config
from src.apps.device.src.mqtt.mqtt_client import MQTTClient

from src.packages.constants.mqtt_topics import MQTTTopic
from src.packages.logger.logger import Logger

logger = Logger("device_main")


def on_activation_message(topic: str, payload: str):
    data = json.loads(payload)

    if data["device_id"] != config.get("id"):
        logger.warn("ID do dispositivo inválido!")
        return

    if data["action"] == "ACTIVATE":
        logger.warn("Abrindo portão...")
        time.sleep(3)
        logger.info("Portão aberto com sucesso!")
    elif data["action"] == "DEACTIVATE":
        logger.warn("Fechando portão...")
        time.sleep(3)
        logger.info("Portão fechado com sucesso!")
    else:
        logger.warn("Ação inválida!")


def rfid_read():
    logger.break_()
    logger.info("Aguardando RFID...")
    rfid = input("=> ")
    if not rfid or len(rfid) != 8:
        logger.warn("Por favor, informe um RFID válido!")
        return None
    return rfid


def _main():
    mqtt_config = config.get("mqtt")
    host, port = mqtt_config.get("host"), mqtt_config.get("port")

    logger.info(f"Starting MQTT client on {host}:{port}...")
    time.sleep(5)

    mqtt = MQTTClient(host, port)
    logger.info("MQTT client started successfully!")

    mqtt.subscribe(MQTTTopic.ACTIVATION.value, on_activation_message)
    mqtt.listen()

    try:
        while True:
            logger.info("Aguardando RFID...")
            rfid = input("=> ")
            if not rfid or len(rfid) != 8:
                logger.warn("Por favor, informe um RFID válido!")
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
        logger.warn("Exiting...")
        exit(0)


_main()
