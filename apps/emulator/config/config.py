import json
import os
from os import path

from apps.emulator.src.utils.log import Log
from packages.config.env import env


class Config:
    """
    A class for handling configuration data and managing a JSON configuration file.
    """

    def __init__(self, file_name="config.json"):
        self._root = path.abspath(path.join(path.dirname(__file__), "../"))
        self._file_path = path.join(self._root, file_name)
        self._data = self.load_config()

    def load_config(self):
        """
        Load the configuration data from the JSON file.
        """
        if self.exists():
            with open(self._file_path) as f:
                return json.load(f)
        else:
            return {}

    def load_default(self):
        """
        Load default configuration data and create the JSON file if it doesn't exist.
        """
        ssid, password, token = env.BOARD_AP_SSID, env.BOARD_AP_PASSWORD, env.BOARD_TOKEN
        if not ssid or not password or not token:
            raise Exception("Missing AP SSID, password or token")

        Log.warn(f"Configuration file not found. Creating a new one at {self._file_path}")
        default_config = {"token": token, "ap": {"ssid": ssid, "password": password}}
        self._data = default_config
        with open(self._file_path, "w") as f:
            json.dump(default_config, f)

    def save_config(self):
        """
        Save the configuration data to the JSON file.
        """
        with open(self._file_path, "w") as f:
            json.dump(self._data, f)

    def get(self, key, default=None):
        """
        Get a configuration value by key, with an optional default value.
        """
        return self._data.get(key, default)

    def set(self, key, value):
        """
        Set a configuration value and save the changes to the JSON file.
        """
        self._data[key] = value
        self.save_config()

    def remove(self, key):
        """
        Remove a configuration key and its associated value from the configuration data and save the changes.
        """
        if key in self._data:
            del self._data[key]
            self.save_config()

    def exists(self):
        """
        Check if the configuration file exists.
        """
        return path.exists(self._file_path)

    def check(self, key: str = None):
        """
        Check if the configuration data is valid.
        """
        if key:
            return key in self._data

        keys = ["id", "mqtt", "wifi"]
        for key in keys:
            if key not in self._data:
                return False
        return True


config = Config()
