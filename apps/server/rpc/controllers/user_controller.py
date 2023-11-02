import typing
import uuid

from apps.server.database import InsertMain, SelectMain
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
        try:
            header_data = SessionHeader(**header)
            if not header_data.token or not header_data.email:
                return BadRequestError("Token ou email não informados").dict()

            if not Security.verify_token(header_data.email, header_data.token):
                return UnauthorizedError("Token inválido").dict()

            data = CreateUserSchema(**payload)
            member = User(
                id=uuid.uuid4(),
                name=data.name,
                email=data.email,
                rfid=data.rfid,
                authorized=data.authorized or True,
                added_by=uuid.UUID(header_data.user_id),
            )

            if InsertMain.insert_user(member):
                LogMaker.write_log(f"User {member.email} created", "info")
                return CreatedResponse(message="Usuário criado com sucesso!", data=True).dict()
            return InternalServerError("Erro ao criar usuário").dict()
        except Exception as e:
            LogMaker.write_log(f"Error: {e}", "error")
            return InternalServerError("Não foi possível processar a requisição").dict()

    @staticmethod
    def select_user(header: typing.Dict[str, typing.Any], user_id: str):
        try:
            header_data = SessionHeader(**header)
            if not header_data.token or not header_data.email:
                return BadRequestError("Token ou email não informados").dict()

            if not Security.verify_token(header_data.email, header_data.token):
                return UnauthorizedError("Token inválido").dict()

            data = SelectMain.select_user(user_id)
            if data:
                return OKResponse(
                    message="Usuário encontrado com sucesso!",
                    data={
                        "id": str(data.id),
                        "name": data.name,
                        "email": data.email,
                        "rfid": data.rfid,
                        "added_by": str(data.added_by),
                        "authorized": data.authorized,
                    },
                ).dict()
            return NotFoundError("Usuário não encontrado").dict()
        except Exception as e:
            LogMaker.write_log(f"Error: {e}", "error")
            return InternalServerError("Não foi possível processar a requisição").dict()

    @staticmethod
    def select_all_users(header: typing.Dict[str, typing.Any]):
        try:
            header_data = SessionHeader(**header)
            if not header_data.token or not header_data.email:
                return BadRequestError("Token ou email não informados").dict()

            if not Security.verify_token(header_data.email, header_data.token):
                return UnauthorizedError("Token inválido").dict()

            users = SelectMain.select_all_users()
            response = []
            for u in users:
                response.append(
                    {
                        "name": u.name,
                        "email": u.email,
                        "rfid": u.rfid,
                        "added_by": str(u.added_by),
                        "id": u.id,
                        "authorized": u.authorized,
                    }
                )
            return OKResponse(message="Usuários listados com sucesso!", data=response).dict()
        except Exception as e:
            LogMaker.write_log(f"Error: {e}", "error")
            return InternalServerError("Não foi possível processar a requisição").dict()
