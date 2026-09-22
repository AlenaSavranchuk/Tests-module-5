from src.main.api.models.mentor.login_user_request import LoginUserRequest
from src.main.api.models.mentor.login_user_response import LoginUserResponse
import requests


class RequestSpecs:
    @staticmethod
    # обычные хэдеры
    def base_headers():
        return {
            "Content-Type": "application/json",
            "accept": "application/json"
        }

    # универсальный метод, который принимает имя и пароль, производит авторизацию, достает из тела
    # ответа токен, и прокидывает его к нашим базовым хэдерам. И теперь эта универсальная конструкция позволяет во всех
    # тестах делать авторизацию через нее и сразу получать нужный нам хэдер
    @staticmethod
    def auth_admin_headers(username: str, password: str):
        request_data = LoginUserRequest(username=username, password=password)
        response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json=request_data.model_dump(),
            headers=RequestSpecs.base_headers()
        )

        if response.status_code == 200:
            response_data = LoginUserResponse(**response.json())
            token = response_data.token
            headers = RequestSpecs.base_headers()
            headers["Authorization"] = f"Bearer {token}"
            return headers # поменяли тут

        raise Exception ('Failed to login')

    @staticmethod
    def unauth_headers():
        return RequestSpecs.base_headers() # поменяли тут
