# Это базовый клиент (CrudRequester) для отправки стандартных HTTP-запросов (POST, DELETE) к API.
# Он изолирует в себе работу с библиотекой requests, автоматически собирает базовый URL
# с эндпоинтом и валидирует ответы сервера, избавляя от дублирования кода в шагах тестов.
import requests
from requests import Response
from src.main.api.configs.config_middle import ConfigMiddle
from src.main.api.foundation.http_requester_senior import HTTPRequesterSenior
from typing import Optional
from pydantic import BaseModel

# Наследуемся от класса HTTPRequester, чтобы получить базовые настройки для работы по HTTP.
# Класс-работяга, унаследованный от базового HTTPRequesterSenior.
# Он берет сохраненные настройки и выполняет реальные сетевые запросы через библиотеку requests.
class CrudRequesterSenior(HTTPRequesterSenior):

    # Метод для отправки POST-запросов. Принимает Pydantic-модель данных для тела запроса.
    def post(self, model: Optional[BaseModel]):
        # Если модель передана, превращаем её в словарь для JSON, если модели нет — оставляем тело пустым "".
        body = model.model_dump() if model is not None else ""

        # Отправляем реальный HTTP POST-запрос на сервер
        response = requests.post(
            # Склеиваем базовый адрес сервера из конфига и относительный путь текущей ручки (эндпоинта)
            url=f"{ConfigMiddle.fetch('backendURL')}{self.endpoint.value.url}",
            # Передаем подготовленные данные в теле запроса
            json=body,
            # Подставляем готовый словарь с заголовками авторизации
            headers=self.request_specs_middle['headers']
        )
        # Вызываем функцию-валидатор, чтобы проверить статус-код ответа (например, что сервер вернул 200 или 201)
        self.response_specs_middle(response)

        # Возвращаем сырой объект ответа сервера обратно для дальнейшего использования
        return response

    # Метод для отправки DELETE-запросов (используется для удаления сущностей по их уникальному ID).
    def delete(self, user_id: int) -> Response:
        # Отправляем реальный HTTP DELETE-запрос на сервер
        response = requests.delete(
            # Формируем динамический URL: добавляем ID удаляемого объекта в самый конец пути через слэш
            url=f"{ConfigMiddle.fetch('backendURL')}{self.endpoint.value.url}/{user_id}",
            # Подставляем заголовки авторизации (например, права администратора для удаления)
            headers=self.request_specs_middle['headers']
        )
        # Проверяем, что удаление прошло успешно на уровне статус-кода сервера
        self.response_specs_middle(response)

        # Возвращаем сырой ответ сервера
        return response




