
from termcolor import colored


class Logger:
    def __init__(self, name: str):
        """
        Initialize the Logger with a name.
        """
        self.name = name.upper()

    def info(self, message: str):
        """
        Log an informational message to the console and file.
        """
        print(colored(f"[{self.name}] {message}", "cyan"))

    def success(self, message: str):
        """
        Log a success message to the console and file.
        """
        print(colored(f"[{self.name}] {message}", "green"))

    def debug(self, message: str):
        """
        Log a debug message to the console and file.
        """
        print(colored(f"[{self.name}] {message}", "purple"))

    def warn(self, message: str):
        """
        Log a warning message to the console and file.
        """
        print(colored(f"[{self.name}] {message}", "yellow"))

    def error(self, message: str):
        """
        Log an error message to the console and file.
        """
        print(colored(f"[{self.name}] {message}", "red"))

    def break_(self):
        """
        Log a separator to the console.
        """
        print("")


if __name__ == "__main__":
    logger = Logger("test")
    logger.info("info")
