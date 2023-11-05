import threading
import typing

import paho.mqtt.client as mqtt


class MQTTClient:
    """
    That class is a wrapper for the MQTT client. It provides a simple interface for
    publishing and subscribing to topics. It also provides a simple callback interface
    for handling incoming messages.
    """

    def __init__(self, host: str, port: int, user: str | None = None, password: str | None = None):
        if not host or not port:
            raise Exception("Missing host or port for MQTTClient")

        self._host: str = host
        self._port: int = port
        self._user: str | None = user
        self._password: str | None = password

        self._client: mqtt.Client = mqtt.Client()
        self._topic_callbacks: dict[str, typing.Callable] = {}

        self._setup_client()

    def _setup_client(self):
        """
        Set up the MQTT client, setting the callbacks and connecting to the broker.
        """
        self._client.on_connect = self._on_connect
        self._client.on_message = self._on_message

        if self._user and self._password:
            self._client.username_pw_set(self._user, self._password)
        self._client.connect(self._host, self._port, 60)

    def _on_connect(self, *args):
        """
        Callback for when the client connects to the broker. Just indicates that the client is connected.
        """
        rc = args[3]
        print(f"[MQTT/CLIENT] Connected with result code {rc}")

    def _on_message(self, *args):
        """
        Callback for when the client receives a message. It calls the callback for the topic if it exists.
        """
        msg = args[2]
        payload = msg.payload.decode()

        print(f"[MQTT/RECEIVED] {msg.topic}: {payload}")
        if self._topic_callbacks.get(msg.topic):
            self._topic_callbacks.get(msg.topic)(topic=msg.topic, payload=payload)

    def _listen(self):
        """
        Starts the client loop, which will listen for incoming messages. It will run until a KeyboardInterrupt is
        """
        try:
            print("[MQTT/CLIENT] Listening...")
            self._client.loop_forever()
        except KeyboardInterrupt:
            print("\n[MQTT/CLIENT] Disconnecting...")
            self._client.disconnect()

    def stop(self):
        """
        Stops the client loop and disconnects from the broker.
        """
        print("\n[MQTT/CLIENT] Disconnecting...")
        self._client.loop_stop()
        self._client.disconnect()

    def listen(self):
        """
        Returns a thread that will listen for incoming messages. It will run until a KeyboardInterrupt is raised.
        """
        mqtt_thread = threading.Thread(target=self._listen)
        mqtt_thread.start()

    def publish(self, topic: str, message: str):
        """
        Publishes a message to a topic.
        """
        print(f"[MQTT/PUBLISHED] {topic}: {message}")
        self._client.publish(topic, message)

    def subscribe(self, topic: str, callback: typing.Callable):
        """
        Subscribes to a topic and sets a callback for when a message is received.
        """
        self._client.subscribe(topic)
        self._topic_callbacks[topic] = callback


if __name__ == "__main__":
    # Just a simple example of how to use the MQTTClient
    from packages.config.env import env

    host, port = env.MQTT_HOST, env.MQTT_PORT
    if not host or not port:
        raise Exception("MQTT_HOST or MQTT_PORT not set")

    mqtt = MQTTClient(host, port)
    mqtt_thread = mqtt.listen().start()

    def on_msg_callback(topic: str, payload: str):
        print(f"[MQTT/CALLBACK] {topic}: {payload}")

    mqtt.subscribe("test", on_msg_callback)
