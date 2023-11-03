from termcolor import colored


class Log:
    @staticmethod
    def info(message: str):
        """
        Log a message to the console.
        """
        print(colored(f"[EMULATOR] {message}", "blue"))

    @staticmethod
    def success(message: str):
        """
        Log a success message to the console.
        """
        print(colored(f"[EMULATOR] {message}", "green"))

    @staticmethod
    def warn(message: str):
        """
        Log a warning message to the console.
        """
        print(colored(f"[EMULATOR] {message}", "yellow"))

    @staticmethod
    def error(message: str):
        """
        Log an error message to the console.
        """
        print(colored(f"[EMULATOR] {message}", "red"))

    @staticmethod
    def break_():
        print("")
