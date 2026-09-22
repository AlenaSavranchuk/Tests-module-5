from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requester.crud_requester import CrudRequester
from src.main.api.foundation.requester.validate_crud_requester import ValidateCrudRequester
from src.main.api.models.mentor import create_user_request
from src.main.api.models.mentor.create_user_request import CreateUserRequest
from src.main.api.models.mentor.login_user_request import LoginUserRequest
from src.main.api.steps.base__steps import BaseSteps
from src.main.api.specs.response_specs_mentor import ResponseSpecs
from src.main.api.specs.request_specs_mentor import RequestSpecs

# Этот класс содержит "шаги" (Steps) администратора для работы с API. Он скрывает за собой
# детали создания реквестеров, подстановку заголовков авторизации (админских или публичных)
# и выбор эндпоинтов, предоставляя тестам понятные методы вроде .create_user() или .delete_user().

# Наследуемся от BaseSteps, чтобы получить доступ к общему списку созданных объектов (self.created_obj).
class AdminSteps(BaseSteps):

    # Шаг для успешного создания нового пользователя администратором.
    def create_user(self, create_user_request: CreateUserRequest):
        # Создаем валидирующий реквестер с админскими правами и ожиданием успешного ответа (200 OK), отправляя POST-запрос.
        response = ValidateCrudRequester(
            RequestSpecs.auth_admin_headers(username='admin', password='123456'),
            # Генерируем заголовки авторизации админа.
            Endpoint.ADMIN_CREATE_USER,  # Передаем конфигурацию ручки создания пользователя.
            ResponseSpecs.request_ok()  # Передаем спецификацию проверки успешного ответа (например, статус 200).
        ).post(create_user_request)

        # Автоматически сохраняем валидированный ответ в список созданных объектов для последующей очистки в фикстуре.
        self.created_obj.append(response)
        # Возвращаем готовую Pydantic-модель ответа обратно в тест.
        return response

    # Шаг для удаления пользователя из системы по его идентификатору.
    def delete_user(self, use_id: int):
        # Используем обычный CrudRequester, так как при удалении нам важен сам факт операции, а не парсинг тела ответа.
        CrudRequester(
            RequestSpecs.auth_admin_headers(username='admin', password='123456'),
            # Подставляем админские заголовки для удаления.
            Endpoint.ADMIN_DELETE_USER,  # Указываем эндпоинт для удаления пользователя.
            ResponseSpecs.request_ok()  # Проверяем, что сервер вернул успешный статус-код.
        ).delete(use_id)  # Вызываем метод удаления, передавая ID пользователя.

    # Негативный шаг: попытка создать некорректного пользователя.
    def create_invalid(self, create_user_request: CreateUserRequest):
        # Используем обычный CrudRequester, так как при ошибке (400 Bad Request) структура JSON-ответа будет другой.
        CrudRequester(
            RequestSpecs.auth_admin_headers(username='admin', password='123456'),
            # Заголовки админа для отправки запроса.
            Endpoint.ADMIN_CREATE_USER,  # Стучимся на ту же ручку создания.
            ResponseSpecs.request_bad()
            # Валидируем, что сервер ответил ошибкой (например, статус 400), как мы и ожидали.
        ).post(create_user_request)

    # Шаг для авторизации (логина) пользователя в системе.
    def login_user(self, login_user_request: LoginUserRequest):
        # Используем ValidateCrudRequester, чтобы на выходе сразу получить модель с токеном авторизации.
        response = ValidateCrudRequester(
            RequestSpecs.unauth_headers(),
            # Используем пустые/неавторизованные заголовки, так как токена у нас еще нет.
            Endpoint.LOGIN_USER,  # Указываем эндпоинт ручки авторизации.
            ResponseSpecs.request_ok()  # Проверяем, что логин прошел успешно.
        ).post(login_user_request)
        # Возвращаем модель с результатом авторизации (токен, сессия).
        return response

