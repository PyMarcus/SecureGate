from functools import wraps

from src.packages.logger.logger import Logger

logger = Logger("command")


def command(cmd: str, args: list[str] | None = None, desc: str = "", public: bool = False):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *cmd_args, **func_kwargs):
            command_info = getattr(wrapper, "_command_info", None)

            if command_info and command_info["args"]:
                expected_args = command_info["args"]
                if len(cmd_args) < len(expected_args):
                    missing_args = expected_args[len(cmd_args) :]
                    formatted_args = (
                        f"{' '.join(f'<{arg}>' for arg in missing_args)}" if missing_args else ""
                    )
                    return logger.warn(f"Argumentos faltantes: {formatted_args}")

            return func(self, *cmd_args, **func_kwargs)

        wrapper._command_info = {
            "command": cmd,
            "args": args or [],
            "description": desc,
            "public": public,
        }

        return wrapper

    return decorator
