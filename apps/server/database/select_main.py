import datetime
import typing
import uuid
from typing import Type

from sqlalchemy import and_
from sqlalchemy.orm import aliased

from packages.schemas.users_schema import UserAccessHistoryJoinSchema

from .config import DBConnection
from .models.__all_models import *
from .models.access_history import AccessHistory


class SelectMain:
    """
    The InsertMain follows the SQLAlchemy's Unit of Work pattern to perform database insertions.
    This pattern is a design pattern used to ensure the consistency of a set of related database operations.
    In the context of SQLAlchemy, the Unit of Work pattern helps in managing database transactions effectively,
    grouping multiple operations into a single unit that either entirely succeeds or fails as a whole.
    """

    __session: DBConnection = DBConnection()

    @classmethod
    def select_admin_by_email(cls, email: str) -> Admin | None:
        try:
            with cls.__session.create_session() as session:
                admin: Admin = session.query(Admin).filter(Admin.email == email).first()
                if admin:
                    return admin
            return None
        except Exception:
            return None

    @classmethod
    def select_admin_by_id(cls, admin_id: str) -> Admin | None:
        try:
            with cls.__session.create_session() as session:
                admin: Admin = session.query(Admin).filter(Admin.id == admin_id).first()
                if admin:
                    return admin
            return None
        except Exception:
            return None

    @classmethod
    def select_user_by_id(cls, user_id: str) -> Admin | None:
        try:
            with cls.__session.create_session() as session:
                user: User = session.query(User).filter(User.id == user_id).first()
                if user:
                    return user
            return None
        except Exception:
            return None

    @classmethod
    def select_user_by_device_id_and_rfid(cls, device_id: str, rfid: str) -> User | None:
        try:
            with cls.__session.create_session() as session:
                user: User = (
                    session.query(User)
                    .filter(User.device_id == device_id)
                    .filter(User.rfid == rfid)
                    .first()
                )
                if user:
                    return user
            return None
        except Exception:
            return None

    @classmethod
    def select_device_by_id(cls, device_id: str) -> Admin | None:
        try:
            with cls.__session.create_session() as session:
                device: Device = session.query(Device).filter(Device.id == device_id).first()
                if device:
                    return device
            return None
        except Exception:
            return None

    @classmethod
    def select_users_by_device_id(cls, device_id: str) -> typing.List[typing.Type[User]] | None:
        try:
            with cls.__session.create_session() as session:
                users: typing.Type[User] = (
                    session.query(User).filter(User.device_id == device_id).all()
                )
                if users:
                    return users
                return None
        except Exception:
            return None

    @classmethod
    def select_root_id(cls) -> uuid.UUID | None:
        try:
            with cls.__session.create_session() as session:
                admin: typing.Type[Admin] = (
                    session.query(Admin).filter(Admin.role == UserRole.ROOT).first()
                )
                if admin:
                    return admin.root_id
                return None
        except Exception:
            return None

    @classmethod
    def select_device_access_history(
        cls, device_id: str, date_ini: str, date_end: str
    ) -> typing.List[AccessHistory] | None:
        try:
            date_ini_obj = datetime.datetime.strptime(date_ini, "%Y-%m-%d %H:%M")
            date_end_obj = datetime.datetime.strptime(date_end, "%Y-%m-%d %H:%M")
            with cls.__session.create_session() as session:
                history: typing.Type[AccessHistory] = (
                    session.query(AccessHistory)
                    .filter(AccessHistory.device_id == device_id)
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
    def select_device_access_history_by_date(
        cls, device_id: str, date: str
    ) -> Type[AccessHistory] | None:
        try:
            with cls.__session.create_session() as session:
                date_obj = datetime.datetime.strptime(date, "%Y-%m-%d")

                history = (
                    session.query(AccessHistory)
                    .filter(AccessHistory.device_id == device_id)
                    .filter(
                        and_(
                            AccessHistory.created_at >= date_obj,
                            AccessHistory.created_at < date_obj + datetime.timedelta(days=1),
                        )
                    )
                    .order_by(AccessHistory.created_at.desc())
                ).all()
                if history:
                    return history
                return None
        except Exception as e:
            print(e)
            return None

    @classmethod
    def select_user_access_history(cls, user_id: str) -> typing.List[AccessHistory] | None:
        try:
            with cls.__session.create_session() as session:
                history: typing.Type[AccessHistory] = (
                    session.query(AccessHistory)
                    .filter(AccessHistory.user_id == user_id)
                    .order_by(AccessHistory.created_at.desc())
                    .all()
                )
                if history:
                    return history
                return None
        except Exception:
            return None

    @classmethod
    def select_user(cls, user_id: str) -> User | None:
        try:
            with cls.__session.create_session() as session:
                user: typing.Type[User] = session.query(User).filter(User.id == user_id).first()
                if user:
                    return user
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
    def select_admins_by_root_id(cls, root_id: str) -> typing.List[Admin]:
        try:
            with cls.__session.create_session() as session:
                admins: typing.Type[Admin] = (
                    session.query(Admin).filter(Admin.root_id == root_id, Admin.id != root_id).all()
                )
                if admins:
                    return admins
                return list()
        except Exception:
            return list()

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
