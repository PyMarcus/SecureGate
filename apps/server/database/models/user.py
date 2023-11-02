import uuid

import sqlalchemy as sa

from .base_model import BaseModel


class User(BaseModel):
    """
    "Authorized or unauthorized individuals regarding access to the gate."
    """

    __tablename__: str = "users"

    id: uuid.UUID = sa.Column(sa.UUID, primary_key=True, default=uuid.uuid4())
    name: str = sa.Column(sa.String(300), nullable=False, unique=True)
    email: str = sa.Column(sa.String(400), nullable=False, unique=True)
    rfid: str = sa.Column(sa.String(300), nullable=False, unique=True)
    authorized: bool = sa.Column(sa.Boolean, nullable=False, default=True)
    added_by: uuid = sa.Column(sa.UUID, sa.ForeignKey("admins.id"), nullable=False)

    def __repr__(self) -> str:
        return f"<User {self.name} - {self.email}"
