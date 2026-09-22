from src.main.api.models.mentor.base_model import BaseModel


# создаем модель для авторизации юзера
class LoginUserRequest(BaseModel):
    username: str
    password: str