from src.main.api.models.mentor.base_model import BaseModel

class User(BaseModel):
    username: str
    role: str


class LoginUserResponse(BaseModel):
    token: str
    user: User

