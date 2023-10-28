from pydantic import BaseModel


class UserSchema(BaseModel):
    name: str
    email: str
    password: str
    root_id: str
    role: str  # 'ADMIN' | 'ROOT'
