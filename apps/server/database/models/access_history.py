import uuid
from datetime import datetime

import sqlalchemy as sa

from .base_model import BaseModel


class AccessHistory(BaseModel):
    __tablename__: str = "access_history"

    id: uuid.UUID = sa.Column(sa.UUID, primary_key=True, default=uuid.uuid4())
    user_id: uuid.UUID = sa.Column(sa.UUID, sa.ForeignKey("users.id"), nullable=False)
    admin_id: uuid.UUID = sa.Column(sa.UUID, sa.ForeignKey("admins.id"), nullable=True)
    device_id: uuid.UUID = sa.Column(sa.UUID, sa.ForeignKey("devices.id"), nullable=False)
    created_at: datetime = sa.Column(sa.DateTime, default=datetime.now, index=True)

    def __str__(self) -> str:
        return f"{self.id} {self.user_id} {self.admin_id} {self.device_id} {self.created_at}"
