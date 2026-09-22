from src.main.api.foundation.http_requester import HTTPRequester
from typing import Optional
from src.main.api.models.mentor.base_model import BaseModel
from requests import Response
import requests
from src.main.api.configs.config_mentor import Config

# Это базовый клиент (CrudRequester) для отправки стандартных HTTP-запросов (POST, DELETE) к API.
# Он изолирует в себе работу с библиотекой requests, автоматически собирает базовый URL
# с эндпоинтом и валидирует ответы сервера, избавляя от дублирования кода в шагах тестов.


# Наследуемся от класса HTTPRequester, чтобы получить базовые настройки для работы по HTTP.
class CrudRequester(HTTPRequester):

    # Метод отправки POST-запроса, который принимает Pydantic-модель данных и возвращает HTTP-ответ.
    def post(self, model: Optional[BaseModel]) -> Response:
        # Если модель передана, превращаем её в Python-словарь через .model_dump() для JSON, иначе оставляем тело пустым.
        body = model.model_dump() if model is not None else ""

        # Выполняем реальный POST-запрос, склеивая адрес хоста из конфига и относительный путь эндпоинта.
        response = requests.post(
            url=f'{Config.fetch("backendUrl")}{self.endpoint.value.url}',  # Формируем полный URL адрес ручки API.
            headers=self.request_specs_mentor,
            # Подставляем обязательные заголовки (например, авторизацию и тип данных).
            json=body  # Передаем подготовленные данные в формате JSON в теле запроса.
        )

        # Проверяем полученный ответ (например, статус-код) с помощью встроенного валидатора спецификаций.
        self.response_specs_mentor(response)

        # Возвращаем объект ответа обратно в шаг теста для дальнейших проверок.
        return response

    # Метод отправки DELETE-запроса для удаления сущности по её уникальному идентификатору (ID).
    def delete(self, user_id: int) -> Response:
        # Выполняем реальный DELETE-запрос, добавляя ID удаляемого объекта в конец URL-адреса.
        response = requests.delete(
            url=f'{Config.fetch("backendUrl")}{self.endpoint.value.url}/{user_id}',
            # Формируем динамический URL для удаления конкретного ID.
            headers=self.request_specs_mentor,  # Подставляем необходимые для выполнения запроса заголовки.
        )

        # Автоматически валидируем ответ сервера (например, ожидая успешный статус 200 или 204).
        self.response_specs_mentor(response)

        # Возвращаем объект ответа сервера в вызывающий метод.
        return response
