import typing
import uuid

from apps.server.database import InsertMain, SelectMain
from apps.server.database.models.__all_models import *
from apps.server.security import Security
from libs import LogMaker
from packages.errors.errors import *
from packages.responses.responses import *
from packages.schemas.admins_schema import AdminSchema
from packages.schemas.session_header import SessionHeader
from packages.schemas.session_schema import *


class AdminController:
    @staticmethod
    def create_admin(header: typing.Dict[str, typing.Any], payload: typing.Dict[str, typing.Any]):
        header_data = SessionHeader(**header)
        if not header_data.token or not header_data.email:
            return BadRequestError("Token ou email não informados").dict()

        data = AdminSchema(**payload)
        if not data.name or not data.email or not data.password or not data.role:
            return BadRequestError("Dados inválidos").dict()

        user = User(
            id=uuid.uuid4(),
            name=data.name,
            email=data.email,
            password=Security.hash_password(data.password),
            root_id=header_data.user_id,
            role=UserRole.ADMIN,
        )

        print(user)
        if InsertMain.insert_user(user):
            LogMaker.write_log(f"Admin {user.email} signed up", "info")
            return CreatedResponse(message="Administrador criado com sucesso!", data=True).dict()
        return BadRequestError("Erro ao criar administrador").dict()
