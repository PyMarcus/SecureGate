from pydantic import BaseModel


class SessionHeader(BaseModel):
    token: str
    email: str
    user_id: str
