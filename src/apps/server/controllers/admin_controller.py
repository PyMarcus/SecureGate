import typing
import uuid

from src.packages.schemas.admins_schema import AdminSchema
from src.packages.schemas.session_header import SessionHeader
from src.packages.database.insert_main import InsertMain
from src.packages.database.models.admin import Admin, UserRole
from src.packages.database.select_main import SelectMain
from src.packages.responses.errors import *

from src.packages.security import Security
from src.packages.logger.logger import Logger
from src.packages.responses.successes import *

logger = Logger("session_controller")


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

            user = Admin(
                id=uuid.uuid4(),
                name=data.name,
                email=data.email,
                password=Security.hash_password(data.password),
                root_id=header_data.user_id,
                role=UserRole.ADMIN,
            )

            if InsertMain.insert_admin(user):
                logger.info(f"Admin {user.email} signed up")
                return CreatedResponse(
                    message="Administrador criado com sucesso!", data=True
                ).dict()
            return BadRequestError("Erro ao criar administrador").dict()
        except Exception as e:
            logger.error(str(e))
            return InternalServerError("Não foi possível processar a requisição").dict()

    @staticmethod
    def select_admin(header: typing.Dict[str, typing.Any], admin_id: str):
        try:
            header_data = SessionHeader(**header)
            if not header_data.token or not header_data.email:
                return BadRequestError("Token ou email não informados").dict()

            if not Security.verify_token(header_data.email, header_data.token):
                return UnauthorizedError("Token inválido").dict()

            data = SelectMain.select_admin_by_id(admin_id)
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
            logger.error(str(e))
            return InternalServerError("Não foi possível processar a requisição").dict()

    @staticmethod
    def select_admins_by_root_id(header: typing.Dict[str, typing.Any], root_id: str):
        try:
            header_data = SessionHeader(**header)
            if not header_data.token or not header_data.email:
                return BadRequestError("Token ou email não informados").dict()

            if not Security.verify_token(header_data.email, header_data.token):
                return UnauthorizedError("Token inválido").dict()

            if not root_id:
                return BadRequestError("Dados inválidos").dict()

            admins = SelectMain.select_admins_by_root_id(root_id)
            response = []
            if admins:
                for a in admins:
                    response.append(
                        {
                            "name": a.name,
                            "email": a.email,
                            "role": a.role.value,
                            "root_id": str(a.root_id),
                            "id": str(a.id),
                        }
                    )
                return OKResponse(message="Admins listados com sucesso!", data=response).dict()
            return NotFoundError("Admins não encontrados").dict()
        except Exception as e:
            logger.error(str(e))
            return InternalServerError("Não foi possível processar a requisição").dict()
