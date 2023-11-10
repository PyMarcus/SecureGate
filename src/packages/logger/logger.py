import os
import logging
from logging.handlers import TimedRotatingFileHandler
from os import path
from termcolor import colored


class Logger:
    def __init__(self, name: str):
        """
        Initialize the Logger with a name.
        """
        self.name = name.upper()
        self.root = path.abspath(path.join(path.dirname(__file__), "../../../"))
        self.dir = path.join(self.root, ".logs")

        os.makedirs(self.dir, exist_ok=True)

        self.format = "%(asctime)s - %(levelname)s - %(message)s"

        self.file_handler = TimedRotatingFileHandler(
            path.join(self.dir, f"{self.name.lower()}.log"), when="midnight", backupCount=7
        )
        self.file_handler.suffix = "%m-%d-%Y"

        self.console_handler = logging.StreamHandler()
        self.console_handler.setFormatter(
            logging.Formatter(self.format))

        logging.basicConfig(
            level=logging.INFO,
            format=self.format,
            handlers=[self.console_handler, self.file_handler],
        )

    def info(self, message: str):
        """
        Log an informational message to the console and file.
        """
        logging.info(f"[{self.name}] {message}")

    def debug(self, message: str):
        """
        Log a debug message to the console and file.
        """
        logging.debug(f"[{self.name}] {message}")

    def warn(self, message: str):
        """
        Log a warning message to the console and file.
        """
        logging.warning(f"[{self.name}] {message}")

    def error(self, message: str):
        """
        Log an error message to the console and file.
        """
        logging.error(f"[{self.name}] {message}")

    def break_(self):
        """
        Log a separator to the console.
        """
        logging.info(colored(f"[{self.name}] {'-' * 50}", "blue"))


if __name__ == "__main__":
    logger = Logger("test")
    logger.info("info")
