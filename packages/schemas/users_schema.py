from pydantic import BaseModel


class CreateUserSchema(BaseModel):
    name: str
    email: str
    rfid: str
    # added_by: str
    authorized: bool
