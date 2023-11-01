import typing
import uuid

from apps.server.database import InsertMain
from apps.server.database.models.__all_models import *
from apps.server.security import Security
from libs import LogMaker
from packages.errors.errors import *
from packages.responses.responses import *
from packages.schemas.session_header import SessionHeader
from packages.schemas.users_schema import CreateUserSchema


class UserController:
    @staticmethod
    def create_user(header: typing.Dict[str, typing.Any], payload: typing.Dict[str, typing.Any]):
        header_data = SessionHeader(**header)
        if not header_data.token or not header_data.email:
            return BadRequestError("Token ou email não informados").dict()

        if Security.verify_token(header_data.email, header_data.token):
            return UnauthorizedError("Token inválido").dict()

        data = CreateUserSchema(**payload)
        member = Member(
            name=data.name,
            email=data.email,
            rfid=data.rfid,
            authorized=data.authorized or True,
            added_by=uuid.UUID(data.added_by),
        )

        if InsertMain.insert_member(member):
            LogMaker.write_log(f"User {member.email} created", "info")
            return CreatedResponse(message="Usuário criado com sucesso!", data=True).dict()
        return InternalServerError("Erro ao criar usuário").dict()
