import typing
import uuid

from .config import DBConnection
from .models.__all_models import *


class UpdateMain:
    """
    The UpdateMain follows the SQLAlchemy's Unit of Work pattern to perform database updates.
    This pattern is a design pattern used to ensure the consistency of a set of related database operations.
    In the context of SQLAlchemy, the Unit of Work pattern helps in managing database transactions effectively,
    grouping multiple operations into a single unit that either entirely succeeds or fails as a whole.
    """

    __session: DBConnection = DBConnection()

    @classmethod
    def update_user_authorization(cls, user_data: typing.Dict[str, typing.Any]) -> bool:
        try:
            with cls.__session.create_session() as session:
                new_authorization = user_data.get("new_authorization")
                user_id = uuid.UUID(user_data.get("user_id"))
                if (
                    new_authorization is None
                    or user_id is None
                    or not isinstance(new_authorization, bool)
                ):
                    return False

                print(user_id)

                user = session.query(User).filter(User.id == user_id).first()

                if user:
                    user.authorized = new_authorization
                    session.commit()
                    return True
                else:
                    print(f"USER {user}")
                    return False
        except Exception as e:
            print(f"Erro ao atualizar autorização do usuário: {e}")
            return False
