import typing
import uuid

from apps.server.database import InsertMain, SelectMain
from apps.server.database.models.__all_models import *
from apps.server.rpc.controllers.authorization_required import authorization_required
from apps.server.security import Security
from libs import LogMaker
from packages.errors.errors import *
from packages.responses.responses import *
from packages.schemas.session_header import SessionHeader
from packages.schemas.users_schema import CreateUserSchema, UserAccessHistoryJoinSchema


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
    @authorization_required
    def select_users_by_device_id(
        header: typing.Dict[str, typing.Any], device_id: str
    ) -> typing.Dict[str, typing.Any]:
        try:
            users: typing.List = SelectMain.select_users_by_device_id(device_id)
            response = []
            if users:
                for user in users:
                    u: UserAccessHistoryJoinSchema = UserAccessHistoryJoinSchema(
                        id=user[0].id,
                        name=user[0].name,
                        email=user[0].name,
                        rfid=user[0].rfid,
                        authorized=user[0].authorized,
                        added_by=user[0].added_by,
                        created_at=user[1],
                        device_id=user[2],
                    )

                    response.append(
                        {
                            "name": u.name,
                            "email": u.email,
                            "rfid": u.rfid,
                            "added_by": str(u.added_by),
                            "id": u.id,
                            "authorized": u.authorized,
                            "time": u.created_at,
                            "device_id": u.device_id,
                        }
                    )
                return OKResponse(message="Usuários listados com sucesso!", data=response).dict()
            return NoContentResponse(message="Sem dados", data={}).dict()
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
