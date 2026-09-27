from src.main.api.models.mentor.base_model import BaseModel

class CreateUserResponse(BaseModel):
    id: int
    username: str
    password: str
    role: str