from src.packages.config.env import env
from src.packages.logger.Logger import Logger

import rpyc

logger = Logger("client")


class Client:
    def __init__(self, host: str, port: int) -> None:
        self._host = host
        self._port = port
        self._uri = f"{self._host}:{self._port}"

    def _connect(self) -> None:
        logger.info(f"Connecting to {self._uri}")
        self._connection = rpyc.connect(self._host, self._port, config={'allow_public_attrs': True})

    def _disconnect(self) -> None:
        logger.info(f"Disconnecting from {self._uri}")
        if self._connection:
            self._connection.close()

    def run(self) -> None:
        self._connect()
        self._disconnect()


if __name__ == "__main__":
    host, port = env.RPC_HOST, env.RPC_PORT
    if not host or not port:
        message = "RPC_HOST or RPC_PORT not set"
        logger.danger(message)

    client = Client(host, port)
    client.run()
