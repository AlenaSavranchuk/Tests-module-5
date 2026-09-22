from pydantic import BaseModel
from typing import Literal

class CreateUserRequestMiddle(BaseModel):
    username: str
    password: str
    role: str



