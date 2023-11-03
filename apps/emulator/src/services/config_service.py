import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from apps.emulator.config.config import config
from apps.emulator.src.utils.log import Log


class HTTPHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        Log.info(format % args)

    def parse_json_request(self) -> dict:
        length = int(self.headers.get("content-length", 0))
        return json.loads(self.rfile.read(length))

    def send_json_response(
        self, status: int = 200, data: any = None, success: bool = True, message: str | None = None
    ):
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        response = {
            "success": success,
            "status_code": status,
            "message": message,
        }
        if data:
            response["data"] = data

        self.wfile.write(json.dumps(response).encode("utf-8"))

    def authenticate(self):
        header = self.headers.get("authorization", None)
        if header:
            token = header.split(" ")[1]
            return token == config.get("token")
        return False

    def do_POST(self):
        if not self.authenticate():
            return self.send_json_response(
                status=401, success=False, message="Token inválido ou não fornecido"
            )

        payload = self.parse_json_request()
        print(payload)

        self.send_json_response(status=200, data={"status": "ok"})


class ConfigService:
    def __init__(self, host: str, port: int):
        self._host = host
        self._port = port
        self._server: HTTPServer | None = None

    def start(self):
        """
        Start the config service.
        """
        try:
            Log.info(f"Starting config service on http://{self._host}:{self._port}")
            self._server = HTTPServer((self._host, self._port), HTTPHandler)
            self._server.serve_forever()
        except KeyboardInterrupt:
            Log.break_()
            Log.danger("Stopping config service")
            self.stop()

    def stop(self):
        """
        Stop the config service.
        """
        self._server.shutdown()
        self._server.server_close()
