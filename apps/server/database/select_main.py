import datetime
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
    def select_user_by_email(cls, email: str) -> User | None:
        try:
            with cls.__session.create_session() as session:
                user: User = session.query(User).filter(User.email == email).first()
                if user:
                    return user
            return None
        except Exception:
            return None

    @classmethod
    def select_user_by_id(cls, user_id: str) -> User | None:
        try:
            with cls.__session.create_session() as session:
                user: User = session.query(User).filter(User.id == user_id).first()
                if user:
                    return user
            return None
        except Exception:
            return None

    @classmethod
    def select_member_by_id(cls, member_id: str) -> User | None:
        try:
            with cls.__session.create_session() as session:
                member: Member = session.query(Member).filter(Member.id == member_id).first()
                if member:
                    return member
            return None
        except Exception:
            return None

    @classmethod
    def select_device_by_id(cls, device_id: str) -> User | None:
        try:
            with cls.__session.create_session() as session:
                device: Device = session.query(Device).filter(Device.id == device_id).first()
                if device:
                    return device
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
    def select_access_history(
        cls, date_ini: str, date_end: str
    ) -> typing.List[AccessHistory] | None:
        try:
            date_ini_obj = datetime.datetime.strptime(date_ini, "%Y-%m-%d %H:%M")
            date_end_obj = datetime.datetime.strptime(date_end, "%Y-%m-%d %H:%M")
            print(date_end_obj, date_ini_obj)
            with cls.__session.create_session() as session:
                history: typing.Type[AccessHistory] = (
                    session.query(AccessHistory)
                    .filter(AccessHistory.created_at.between(date_ini_obj, date_end_obj))
                    .all()
                )
                if history:
                    return history
                return None
        except Exception as e:
            print(e)
            return None

    @classmethod
    def select_member(cls, id: str) -> Member | None:
        try:
            with cls.__session.create_session() as session:
                member: typing.Type[Member] = session.query(Member).filter(Member.id == id).first()
                if member:
                    return member
                return None
        except Exception:
            return None

    @classmethod
    def select_device(cls, id: str) -> Device | None:
        try:
            with cls.__session.create_session() as session:
                device: typing.Type[Device] = session.query(Device).filter(Device.id == id).first()
                if device:
                    return device
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

    @classmethod
    def select_all_devices(cls) -> typing.List[Device]:
        try:
            with cls.__session.create_session() as session:
                devices: typing.Type[Device] = session.query(Device).all()
                if devices:
                    return devices
                return list()
        except Exception:
            return list()

    @classmethod
    def select_all_access_history(cls) -> typing.List[AccessHistory]:
        try:
            with cls.__session.create_session() as session:
                history: typing.Type[AccessHistory] = session.query(AccessHistory).all()
                if history:
                    return history
                return list()
        except Exception:
            return list()
