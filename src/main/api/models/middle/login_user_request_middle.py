from pydantic import BaseModel

class LoginUserRequestMiddle(BaseModel):
    username: str
    password: str



