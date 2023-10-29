from .config import DBConnection
from .models.__all_models import *


class InsertMain:
    """
    The InsertMain follows the SQLAlchemy's Unit of Work pattern to perform database insertions.
    This pattern is a design pattern used to ensure the consistency of a set of related database operations.
    In the context of SQLAlchemy, the Unit of Work pattern helps in managing database transactions effectively,
    grouping multiple operations into a single unit that either entirely succeeds or fails as a whole.
    """

    __session: DBConnection = DBConnection()

    @classmethod
    def insert_user(cls, user: User) -> bool:
        try:
            with cls.__session.create_session() as session:
                session.add(user)
                session.commit()
            return True
        except Exception as e:
            print(e)
            return False

    @classmethod
    def insert_member(cls, member: Member) -> bool:
        try:
            with cls.__session.create_session() as session:
                session.add(member)
                session.commit()
                return True
        except Exception:
            return False

    @classmethod
    def insert_device(cls, device: Device) -> bool:
        try:
            with cls.__session.create_session() as session:
                session.add(device)
                session.commit()
                return True
        except Exception:
            return False
