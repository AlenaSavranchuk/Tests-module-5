# Этот класс является "Отделом технического контроля" (прорабом) нашего фреймворка.
# Он наследует базовые настройки от HTTPRequesterSenior и оборачивает работу низкоуровневого
# CrudRequesterSenior. Его главная цель — взять сырой ответ от сервера, принудительно
# перепроверить его статус-код на верхнем уровне (фишка ментора для гибкости в тестах)
# и автоматически превратить JSON-текст в готовую, строго проверенную Pydantic-модель.

from src.main.api.foundation.http_requester_senior import HTTPRequesterSenior
from src.main.api.foundation.requester.crud_requester_senior import CrudRequesterSenior
from pydantic import BaseModel
from typing import Optional


class ValidateCrudRequesterSenior(HTTPRequesterSenior):
    # Конструктор принимает эндпоинт, спецификацию (хедеры) запроса и функцию проверки ответа.
    def __init__(self, endpoint, request_specs_middle, response_specs_middle):
        # Передаем все три параметра в родительский класс, чтобы они сохранились в self.
        super().__init__(endpoint, request_specs_middle, response_specs_middle)
        # Создаем внутри экземпляр работяги CrudRequesterSenior, передавая ему те же настройки для сетевой работы.
        # Внимание: убедись, что имена именованных аргументов (request_specs_middle, endpoint) точно
        # совпадают с тем, как они объявлены в конструкторе класса CrudRequesterSenior.
        self.crud_requester_senior = CrudRequesterSenior(
            endpoint=endpoint,
            request_specs_middle=request_specs_middle,
            response_specs_middle=response_specs_middle
        )

    # Умный метод для отправки POST-запросов, который возвращает проверенную Pydantic-модель.
    def post(self, model: Optional[BaseModel] = None) -> BaseModel:
        # Делегируем грязную работу работяге и получаем от него сырой HTTP-ответ.
        response = self.crud_requester_senior.post(model)
        # Принудительно вызываем функцию-спецификацию для проверки статус-кода ответа на этом уровне.
        self.response_specs_middle(response)
        # Извлекаем из нашей карты API модель ответа для этой ручки и валидируем через нее JSON сервера.
        return self.endpoint.value.response_model.validate(response.json())

    # Умный метод для отправки DELETE-запросов, который возвращает модель данных после удаления.
    def delete(self, user_id: int) -> BaseModel:
        # Отправляем запрос на удаление через внутренний экземпляр работяги.
        response = self.crud_requester_senior.delete(user_id)
        # Перепроверяем, что сервер ответил успешным статус-кодом.
        self.response_specs_middle(response)
        # Парсим JSON-результат удаления в строгую Pydantic-модель, привязанную к этому эндпоинту.
        return self.endpoint.value.response_model.validate(response.json())
