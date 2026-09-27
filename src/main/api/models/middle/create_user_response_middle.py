from pydantic import BaseModel

class CreateUserResponseMiddle(BaseModel):
    id: int
    username: str
    password: str
    role: str
