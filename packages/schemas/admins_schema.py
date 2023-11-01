from pydantic import BaseModel


class AdminSchema(BaseModel):
    name: str
    email: str
    password: str
    role: str  # 'ADMIN'
