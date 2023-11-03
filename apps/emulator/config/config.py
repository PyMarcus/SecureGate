import json
import os
from os import path

from apps.emulator.src.utils.log import Log


class Config:
    """
    A class for handling configuration data and managing a JSON configuration file.
    """

    def __init__(self, file_path="config.json"):
        self.file_path = file_path
        self.data = self.load_config()

    def load_config(self):
        """
        Load the configuration data from the JSON file.
        """
        if self.file_path in os.listdir():
            with open(self.file_path) as f:
                return json.load(f)
        else:
            return {}

    def load_default(self):
        """
        Load default configuration data and create the JSON file if it doesn't exist.
        """
        Log.warn(f"Configuration file not found. Creating a new one at {self.file_path}")
        default_config = {"ap": {"ssid": "secure_gate", "password": "12345678"}}
        self.data = default_config
        with open("config.json", "w") as f:
            json.dump(default_config, f)

    def save_config(self):
        """
        Save the configuration data to the JSON file.
        """
        with open(self.file_path, "w") as f:
            json.dump(self.data, f)

    def get(self, key, default=None):
        """
        Get a configuration value by key, with an optional default value.
        """
        return self.data.get(key, default)

    def set(self, key, value):
        """
        Set a configuration value and save the changes to the JSON file.
        """
        self.data[key] = value
        self.save_config()

    def remove(self, key):
        """
        Remove a configuration key and its associated value from the configuration data and save the changes.
        """
        if key in self.data:
            del self.data[key]
            self.save_config()

    def exists(self):
        """
        Check if the configuration file exists.
        """
        return path.exists(self.file_path)

    def check(self, key: str = None):
        """
        Check if the configuration data is valid.
        """
        if key:
            return key in self.data

        keys = ["id", "mqtt", "wifi"]
        for key in keys:
            if key not in self.data:
                return False
        return True


config = Config()
