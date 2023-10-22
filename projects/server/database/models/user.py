import uuid
import sqlalchemy as sa
from datetime import datetime
from .base_model import BaseModel


class User(BaseModel):
    __tablename__: str = "users"

    id: uuid.UUID = sa.Column(sa.UUID, primary_key=True, default=uuid.uuid4)
    created_at: datetime = sa.Column(sa.DateTime, default=datetime.now, index=True)
    name: str = sa.Column(sa.String(200), unique=True, nullable=False)
    email: str = sa.Column(sa.String(250), unique=True, nullable=False)
    password: str = sa.Column(sa.String(500), nullable=False)

    def __repr__(self) -> str:
        return f"<User: {self.name} - {self.email}>"
