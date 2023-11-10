import typing
import uuid

from src.packages.database.insert_main import InsertMain
from src.packages.database.models.admin import Admin, UserRole
from src.packages.database.select_main import SelectMain
from src.packages.responses.errors import *
from src.packages.schemas.session_schema import SigninSchema, SignupSchema

from src.packages.security import Security
from src.packages.logger.logger import Logger
from src.packages.responses.successes import *

logger = Logger("session_controller")


class SessionController:

    @staticmethod
    def sign_in(payload: typing.Dict[str, typing.Any]):
        try:
            data = SigninSchema(**payload)
            if not data.email or not data.password:
                return BadRequestError("Dados inválidos").dict()

            user = SelectMain.select_admin_by_email(data.email)
            if not user:
                return NotFoundError("Usuário não encontrado").dict()

            hashed_password = user.password

            if not Security.verify_password(hashed_password, data.password):
                return BadRequestError("Email ou senha inválidos").dict()
            logger.info(f"User {user.email} signed in")

            return OKResponse(
                message="Sign in realizado com sucesso!",
                data={
                    "user_id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "role": user.role,
                    "token": Security.generate_token(user.email),
                },
            ).dict()
        except Exception as e:
            logger.error(str(e))
            return InternalServerError("Não foi possível processar a requisição").dict()

    @staticmethod
    def sign_up(payload: dict):
        try:
            data = SignupSchema(**payload)
            if not data.name or not data.email or not data.password or not data.role:
                return BadRequestError("Dados inválidos").dict()

            user_id = uuid.uuid4()
            user = Admin(
                id=user_id,
                name=data.name,
                email=data.email,
                password=Security.hash_password(data.password),
                root_id=user_id,
                role=UserRole.ROOT,
            )
            if InsertMain.insert_admin(user):
                logger.info(f"User {user.email} signed up")
                return CreatedResponse(message="Usuário criado com sucesso!", data=True).dict()
            return BadRequestError("Erro ao criar usuário").dict()
        except Exception as e:
            logger.error(str(e))
            return InternalServerError("Não foi possível processar a requisição").dict()
