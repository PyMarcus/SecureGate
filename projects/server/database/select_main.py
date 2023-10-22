from .config import DBConnection
from .models.__all_models import *


class SelectMain:
    """
    The InsertMain follows the SQLAlchemy's Unit of Work pattern to perform database insertions.
    This pattern is a design pattern used to ensure the consistency of a set of related database operations.
    In the context of SQLAlchemy, the Unit of Work pattern helps in managing database transactions effectively,
    grouping multiple operations into a single unit that either entirely succeeds or fails as a whole.
    """

    __session: DBConnection = DBConnection()

    @classmethod
    def select_user(cls, email: str) -> User | None:
        try:
            with cls.__session.create_session() as session:
                user: User = session.query(User).filter(User.email == email).first()
                if user:
                    return user
            return None
        except Exception as e:
            return None
