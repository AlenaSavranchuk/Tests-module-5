# Это архитектурный контракт (закон) проекта. Он ничего сам не делает, но заставляет
# любой класс-отправщик запросов иметь именно эти три метода. Тесты будут вызывать
# интерфейс CrudEndpointSenior, благодаря чему мы сможем легко подменять обычного
# работягу (CrudRequester) на умного прораба (ValidateCrudRequester) без переписывания тестов.

from typing import Protocol, Optional
from pydantic import BaseModel
from requests import Response


class CrudEndpointSenior(Protocol):

    # ЗАЧЕМ ТУТ ТИП "BaseModel | Response":
    # Знак "|" означает "ИЛИ". Мы заявляем, что этот метод гибкий.
    # Обычный работяга (CrudRequester) вернет сырой ответ сервера -> Response.
    # А продвинутый прораб (ValidateCrudRequester) вернет уже готовую модель -> BaseModel.
    # Контракт разрешает оба варианта, чтобы мы могли использовать класс в любых кейсах.
    def post(self, model: Optional[BaseModel]) -> BaseModel | Response:
        ...  # Три точки означают, что здесь нет логики. Это просто описание правила.

    # ЗАЧЕМ ТУТ ТИП "BaseModel | Response":
    # Метод GET запрашивает данные по ID. Он тоже может вернуть либо сырой ответ сервера
    # (например, если мы проверяем ошибку 404), либо успешно собранную Pydantic-модель объекта.
    def get(self, user_id: int) -> BaseModel | Response:
        ...

    # ЗАЧЕМ ТУТ ТИП "BaseModel | Response":
    # Метод DELETE удаляет объект. Чаще всего он возвращает пустой Response со статусом 204,
    # но некоторые API в ответ присылают JSON с моделью успешного удаления (например, DeleteUserResponse).
    # Тип "ИЛИ" защищает нас на оба этих случая.
    def delete(self, user_id: int) -> BaseModel | Response:
        ...


...