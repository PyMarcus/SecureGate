from pydantic import BaseModel


class AdminSchema(BaseModel):
    name: str
    email: str
    password: str
    root_id: str
    role: str  # 'ADMIN' | 'ROOT'
