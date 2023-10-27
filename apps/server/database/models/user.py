import typing
import uuid
from datetime import datetime
from enum import Enum as E

import sqlalchemy as sa

from .base_model import BaseModel


class UserRole(E):
    ROOT = "root"
    ADMIN = "admin"


class User(BaseModel):
    __tablename__: str = "users"

    id: uuid.UUID = sa.Column(sa.UUID, primary_key=True, default=uuid.uuid4)
    root_id: uuid.UUID = sa.Column(sa.UUID, nullable=False)
    created_at: datetime = sa.Column(sa.DateTime, default=datetime.now, index=True)
    name: str = sa.Column(sa.String(200), unique=True, nullable=False)
    email: str = sa.Column(sa.String(250), unique=True, nullable=False)
    password: str = sa.Column(sa.String(500), nullable=False)
    role = sa.Column(sa.Enum(UserRole), default=UserRole.ADMIN)

    def __repr__(self) -> str:
        return f"<User: {self.name} - {self.email}>"
