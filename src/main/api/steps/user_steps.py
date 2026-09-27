from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requester.validate_crud_requester import ValidateCrudRequester
from src.main.api.models.mentor.create_user_request import CreateUserRequest
from src.main.api.specs.request_specs_mentor import RequestSpecs
from src.main.api.specs.response_specs_mentor import ResponseSpecs
from src.main.api.steps.base__steps import BaseSteps

# ЗАЧЕМ НУЖЕН ЭТОТ ФАЙЛ / ФРАГМЕНТ:
# Этот класс содержит шаги (Steps) обычного пользователя. Он инкапсулирует логику
# взаимодействия с клиентскими ручками API, используя динамические заголовки
# авторизации на основе переданных данных конкретного пользователя.

# Наследуемся от BaseSteps, чтобы иметь доступ к общему списку созданных объектов.
class UserSteps(BaseSteps):

    # Шаг для создания личного аккаунта пользователем под своими учетными данными.
    def create_account(self, create_user_request: CreateUserRequest):
        # Используем ValidateCrudRequester, чтобы автоматически проверить структуру JSON-ответа и вернуть готовую Pydantic-модель.
        response = ValidateCrudRequester(
            # Динамически генерируем заголовки авторизации, используя персональные username и password из переданного запроса.
            RequestSpecs.auth_admin_headers(username=create_user_request.username,
                                            password=create_user_request.password),
            Endpoint.CREATE_ACCOUNT,  # Указываем эндпоинт ручки создания аккаунта.
            ResponseSpecs.request_created()
            # Проверяем, что сервер вернул статус-код успешного создания (например, 201 Created).
        ).post()  # Вызываем POST-запрос (без передачи тела, так как данные авторизации уже ушли в headers).

        # Возвращаем проверенную и заполненную модель аккаунта обратно в тест.
        return response
