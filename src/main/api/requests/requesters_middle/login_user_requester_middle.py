from src.main.api.requests.requesters_middle.requester_middle import RequesterMiddle
import requests
from src.main.api.models.middle.login_user_request_middle import LoginUserRequestMiddle
from src.main.api.models.middle.login_user_response_middle import LoginUserResponseMiddle

class LoginUserRequesterMiddle(RequesterMiddle):
    def post(self, login_user_request_middle: LoginUserRequestMiddle): # сюда всегда передаем модель запроса только, ответ мы делаем в return
        url = f'{self.base_url}/api/auth/token/login'
        response = requests.post(
            url = url,
            json = login_user_request_middle.model_dump(),
            headers = self.headers
        )
        self.response_speck_middle(response)
        return LoginUserResponseMiddle(**response.json())