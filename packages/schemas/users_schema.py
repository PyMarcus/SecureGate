from pydantic import BaseModel


class CreateUserSchema(BaseModel):
    name: str
    email: str
    rfid: str
    # added_by: str
    authorized: bool

    def __str__(self) -> str:
        return f"{self.name} {self.email} {self.rfid} {self.authorized}"
