import typing
import uuid

from src.packages.database.models.user import User
from src.packages.database.update_main import UpdateMain
from src.packages.responses.errors import *
from src.packages.logger.logger import Logger
from src.packages.security import Security
from src.packages.database.insert_main import InsertMain
from src.packages.database.select_main import SelectMain
from src.packages.responses.successes import *
from src.packages.schemas.session_header import SessionHeader
from src.packages.schemas.users_schema import CreateUserSchema

logger = Logger("user_controller")


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
            user = User(
                id=uuid.uuid4(),
                name=data.name,
                email=data.email,
                rfid=data.rfid,
                device_id=uuid.UUID(data.device_id),
                authorized=data.authorized,
                added_by=uuid.UUID(header_data.user_id),
            )

            if InsertMain.insert_user(user):
                logger.info(f"User {user.email} created")
                return CreatedResponse(message="Usuário criado com sucesso!", data=True).dict()
            return InternalServerError("Erro ao criar usuário").dict()
        except Exception as e:
            logger.error(str(e))
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
            logger.error(str(e))
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
            logger.error(str(e))
            return InternalServerError("Não foi possível processar a requisição").dict()

    @staticmethod
    def update_user_authorization(
            header: typing.Dict[str, str], user: typing.Dict[str, typing.Any]
    ) -> typing.Dict[str, typing.Any]:
        try:
            header_data = SessionHeader(**header)
            if not header_data.token or not header_data.email:
                return BadRequestError("Token ou email não informados").dict()

            if not Security.verify_token(header_data.email, header_data.token):
                return UnauthorizedError("Token inválido").dict()

            if UpdateMain.update_user_authorization(user):
                return OKResponse(
                    message="Permissao de usuário atualizada com sucesso!", data=True
                ).dict()
            return InternalServerError(
                "Não foi possível atualizar o usuario, verifique os dados"
            ).dict()
        except Exception as e:
            logger.error(str(e))
            return InternalServerError("Não foi possível processar a requisição").dict()

    @staticmethod
    def authenticate_user_rfid(device_id: str, rfid: str):
        try:
            user = SelectMain.select_user_by_device_id_and_rfid(device_id, rfid)
            return user
        except Exception as e:
            logger.error(str(e))
            return None
