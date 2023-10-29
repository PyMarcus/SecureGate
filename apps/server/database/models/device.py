import uuid

import sqlalchemy as sa

from .base_model import BaseModel


class Device(BaseModel):
    __tablename__: str = "devices"

    id: uuid.UUID = sa.Column(sa.UUID, primary_key=True, default=uuid.uuid4())
    name: str = sa.Column(sa.String(200), unique=True, nullable=False)
    wifi_ssid: str = sa.Column(sa.String(200), unique=True, nullable=False)
    wifi_password: str = sa.Column(sa.String(500), nullable=False)
    version: str = sa.Column(sa.String(200))
