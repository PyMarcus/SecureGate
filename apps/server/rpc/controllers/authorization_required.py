import typing

from apps.server.security import Security
from packages.errors.errors import BadRequestError, UnauthorizedError
from packages.schemas.session_header import SessionHeader


def authorization_required(function: typing.Callable) -> typing.Any:
    def wrapper(*args):
        header_data = SessionHeader(**args[0])
        if not header_data.token or not header_data.email:
            return BadRequestError("Token ou email não informados").dict()

        if not Security.verify_token(header_data.email, header_data.token):
            return UnauthorizedError("Token inválido").dict()
        return function(*args)

    return wrapper
