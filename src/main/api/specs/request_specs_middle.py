# в этом файле мы реализуем шаблон для запросов, а именно, его хэдэры
import requests

from src.main.api.configs.config_middle import ConfigMiddle
from src.main.api.models.middle.login_user_request_middle import LoginUserRequestMiddle
from src.main.api.models.middle.login_user_response_middle import  LoginUserResponseMiddle


class RequestSpecs:
    @staticmethod
    # базовые хэдеры для всего, возвращает чистый словарь
    def base_headers():
        return {'accept':'application/json','Content-Type':'application/json'}

    @staticmethod
    # возвращает комплекты (базовые хэдеры+url)
    def unauth_headers():
        return {
            'headers': RequestSpecs.base_headers(),
            'base_url': ConfigMiddle.fetch('backendURL')
        }

    @staticmethod
    # делает авто-логин, достает токен, берет базовые хэдеры, добавляет в них токен прямо на месте и возвращает комплект хэдеры с токеном + url
    def auth_admin_headers(username, password):
        headers = RequestSpecs.base_headers()
        request_data = LoginUserRequestMiddle(username=username, password=password)
        response = requests.post(
            url = f"{ConfigMiddle.fetch('backendURL')}/auth/token/login",
            json = request_data.model_dump(),
            headers = RequestSpecs.base_headers()
        )

        if response.status_code == 200:
            response_data = LoginUserResponseMiddle(**response.json())
            token = response_data.token
            headers['Authorization'] = f'Bearer {token}'
            return {
                'headers': headers,
                'base_url': ConfigMiddle.fetch('backendURL')
            }
        raise Exception('Failed to login')

