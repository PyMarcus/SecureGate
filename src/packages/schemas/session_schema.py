from pydantic import BaseModel


class SigninSchema(BaseModel):
    email: str
    password: str


class SignupSchema(BaseModel):
    name: str
    email: str
    password: str
    role: str  # 'ROOT'


class Session(BaseModel):
    token: str
    user_id: str
    name: str
    email: str
