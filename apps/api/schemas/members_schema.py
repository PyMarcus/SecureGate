from pydantic import BaseModel


class MemberSignUpSchema(BaseModel):
    name: str
    email: str
    rfid: str
    added_by: str  # 'ADMIN' | 'ROOT'
