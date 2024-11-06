from pydantic import BaseModel, ConfigDict
from datetime import datetime


class User(BaseModel):
    username: str


class UserRegister(User):
    password: str


class UserOut(User):
    id: int
    registered_at: datetime

    model_config = ConfigDict(from_attributes=True)
