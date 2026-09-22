# делим на позитивные и негативные сценарии, этот файл отвечает за позитивный, он возвращает пайтон объект(распакаовывть объект в модели и возвращать нам это в тесты
from src.main.api.foundation.http_requester import HTTPRequester
from src.main.api.foundation.requester.crud_requester import CrudRequester
from src.main.api.models.mentor.base_model import BaseModel
from typing import Optional

# ЗАЧЕМ НУЖЕН ЭТОТ ФАЙЛ / ФРАГМЕНТ:
# Этот класс расширяет обычный клиент (CrudRequester), добавляя автоматическую десериализацию.
# Он не просто отправляет запросы, а автоматически превращает сырой JSON-ответ от сервера
# в строгую Pydantic-модель (объект) и валидирует её структуру на соответствие схеме.

# Класс-валидатор унаследован от HTTPRequester для работы со спецификациями запросов и ответов.
class ValidateCrudRequester(HTTPRequester):

    # Конструктор принимает спецификации, эндпоинт и сразу инициализирует внутри себя базовый CrudRequester.
    def __init__(self, request_specs_mentor, endpoint, response_specs_mentor):
        # Вызываем конструктор родительского класса HTTPRequester для сохранения базовых настроек.
        super().__init__(request_specs_mentor, endpoint, response_specs_mentor)

        # Создаем экземпляр обычного CrudRequester, делегируя ему низкоуровневую отправку HTTP-запросов.
        self.crud_requester = CrudRequester(
            request_specs_mentor=request_specs_mentor,
            endpoint=endpoint,
            response_specs_mentor=response_specs_mentor
        )

    # Метод отправляет POST-запрос, проверяет его и возвращает уже готовую, проверенную Pydantic-модель данных.
    def post(self, model: Optional[BaseModel] = None) -> BaseModel:
        # Отправляем запрос через сохраненный ранее crud_requester и получаем сырой HTTP-ответ.
        response = self.crud_requester.post(model)

        # Валидируем общие параметры ответа (например, статус-код) через спецификацию ментора.
        self.response_specs_mentor(response)

        # Парсим JSON-ответ и проверяем его структуру на соответствие ожидаемой Pydantic-модели эндпоинта.
        return self.endpoint.value.response_model.validate(response.json())

    # Метод удаляет объект по ID, проверяет ответ сервера и парсит результат в Pydantic-модель.
    def delete(self, user_id: int):
        # Выполняем удаление через базовый crud_requester и сохраняем ответ.
        response = self.crud_requester.delete(user_id)

        # Проверяем корректность ответа (статус-код) согласно правилам спецификации.
        self.response_specs_mentor(response)

        # Проверяем структуру тела ответа после удаления и возвращаем её в виде готового объекта.
        return self.endpoint.value.response_model.validate(response.json())


