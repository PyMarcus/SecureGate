from src.packages.config.env import env

from rpyc import Service
from rpyc.utils.server import ThreadedServer

from src.packages.constants.mqtt_topics import MQTTTopic
from src.packages.logger.Logger import Logger
from src.packages.mqtt.mqtt_client import MQTTClient

logger = Logger(__name__


class Server(Service):
    def __init__(self, host: str, port: int) -> None:
        self._host = host
        self._port = port

        self._setup_mqtt()
        self._subscribe_mqtt_topics()
        self._setup_controller()

    def _setup_mqtt(self) -> None:
        host, port = env.MQTT_HOST, env.MQTT_PORT
        if not host or not port:
            message = "MQTT_HOST or MQTT_PORT not set"
            logger.danger(message)
            raise Exception(message)

        self._mqtt = MQTTClient(host, port)
        self._mqtt.listen()

    def _subscribe_mqtt_topics(self) -> None:
        self._mqtt.subscribe(MQTTTopic.AUTHENTICATION.value, self.handle_rfid_auth)

    def _setup_controller(self) -> None:
        # self._device_controller = DeviceController(self._mqtt)
        pass

    def run(self) -> None:
        thread = ThreadedServer(self, hostname=self._host, port=self._port)
        thread.start()

    def handle_rfid_auth(self, topic: str, payload: str) -> None:
        pass




if __name__ == "__main__":
    server = ThreadedServer(Server(env("SERVER_HOST"), env("SERVER_PORT")))
    server.start()
