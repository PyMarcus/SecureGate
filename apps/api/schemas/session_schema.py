from pydantic import BaseModel


class Signin(BaseModel):
    email: str
    password: str


class Signup(BaseModel):
    username: str
    email: str
    password: str
    # role: str #  'ADMIN' | 'ROOT'
