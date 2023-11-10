import datetime
import typing

from pydantic import BaseModel


class CreateUserSchema(BaseModel):
    name: str
    email: str
    rfid: str
    # added_by: str
    authorized: bool
    device_id: str


class UpdateUserAuthorizedSchema(BaseModel):
    user_id: str
    new_authorization: bool


class UserAccessHistoryJoinSchema(BaseModel):
    id: typing.Any
    name: str
    email: str
    rfid: str
    authorized: bool
    added_by: typing.Any
    created_at: datetime.datetime
    device_id: typing.Any
