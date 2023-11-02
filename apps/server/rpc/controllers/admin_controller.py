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
        try:
            header_data = SessionHeader(**header)
            if not header_data.token or not header_data.email:
                return BadRequestError("Token ou email não informados").dict()

            if not Security.verify_token(header_data.email, header_data.token):
                return UnauthorizedError("Token inválido").dict()

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
                return CreatedResponse(
                    message="Administrador criado com sucesso!", data=True
                ).dict()
            return BadRequestError("Erro ao criar administrador").dict()
        except Exception as e:
            LogMaker.write_log(f"Error: {e}", "error")
            return InternalServerError("Não foi possível processar a requisição").dict()

    @staticmethod
    def select_admin(header: typing.Dict[str, typing.Any], admin_id: str):
        try:
            header_data = SessionHeader(**header)
            if not header_data.token or not header_data.email:
                return BadRequestError("Token ou email não informados").dict()

            if not Security.verify_token(header_data.email, header_data.token):
                return UnauthorizedError("Token inválido").dict()

            data = SelectMain.select_user_by_id(admin_id)
            if data:
                return OKResponse(
                    message="Administrador encontrado com sucesso!",
                    data={
                        "id": str(data.id),
                        "name": data.name,
                        "email": data.email,
                        "role": data.role,
                    },
                ).dict()
            return NotFoundError("Administrador não encontrado").dict()
        except Exception as e:
            LogMaker.write_log(f"Error: {e}", "error")
            return InternalServerError("Não foi possível processar a requisição").dict()

    @staticmethod
    def select_all_admins(header: typing.Dict[str, typing.Any]):
        try:
            header_data = SessionHeader(**header)
            if not header_data.token or not header_data.email:
                return BadRequestError("Token ou email não informados").dict()

            if not Security.verify_token(header_data.email, header_data.token):
                return UnauthorizedError("Token inválido").dict()

            admins = SelectMain.select_all_users()
            response = []
            for a in admins:
                response.append(
                    {
                        "name": a.name,
                        "email": a.email,
                        "role": a.role,
                        "root_id": a.root_id,
                        "id": a.id,
                    }
                )
            return OKResponse(message="Admins listados com sucesso!", data=response).dict()
        except Exception as e:
            LogMaker.write_log(f"Error: {e}", "error")
            return InternalServerError("Não foi possível processar a requisição").dict()
