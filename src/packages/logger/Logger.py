from termcolor import colored


class Logger:
    def __init__(self, name: str):
        self.name = name.upper()

    def info(self, message: str):
        """
        Log a message to the console.
        """
        print(colored(f"[{self.name}] {message}", "blue"))

    def success(self, message: str):
        """
        Log a success message to the console.
        """
        print(colored(f"[{self.name}] {message}", "green"))

    def warn(self, message: str):
        """
        Log a warning message to the console.
        """
        print(colored(f"[{self.name}] {message}", "yellow"))

    def danger(self, message: str):
        """
        Log an error message to the console.
        """
        print(colored(f"[{self.name}] {message}", "red"))

    def break_(self):
        print("")
