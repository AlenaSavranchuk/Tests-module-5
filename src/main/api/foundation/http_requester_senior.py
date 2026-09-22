# Базовый движок (клиент) для отправки HTTP-запросов.
# Инкапсулирует логику работы с сессией, заголовками и эндпоинтами,
# автоматически связывая конфигурацию ручки с отправкой данных.
from typing import  Dict, Callable
from src.main.api.foundation.endpoint import Endpoint

class HTTPRequesterSenior:
    # тут тип данных дикт потому что спека запроса отправляет словарь, а спека ответа отправляет нам функцию
    def __init__(self, endpoint: Endpoint, request_specs_middle: Dict, response_specs_middle: Callable):
        self.endpoint = endpoint
        self.request_specs_middle = request_specs_middle
        self.response_specs_middle = response_specs_middle
