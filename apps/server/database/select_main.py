import typing
import uuid

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
        except Exception:
            return None

    @classmethod
    def select_root_id(cls) -> uuid.UUID | None:
        try:
            with cls.__session.create_session() as session:
                user: typing.Type[User] = (
                    session.query(User).filter(User.role == UserRole.ROOT).first()
                )
                if user:
                    return user.root_id
                return None
        except Exception:
            return None

    @classmethod
    def select_member(cls, email: str) -> Member | None:
        try:
            with cls.__session.create_session() as session:
                member: typing.Type[Member] = (
                    session.query(Member).filter(Member.email == email).first()
                )
                if member:
                    return member
                return None
        except Exception:
            return None

    @classmethod
    def select_all_users(cls) -> typing.List[User]:
        try:
            with cls.__session.create_session() as session:
                users: typing.Type[User] = session.query(User).all()
                if users:
                    return users
                return list()
        except Exception:
            return list()

    @classmethod
    def select_all_members(cls) -> typing.List[Member]:
        try:
            with cls.__session.create_session() as session:
                members: typing.Type[Member] = session.query(Member).all()
                if members:
                    return members
                return list()
        except Exception:
            return list()
