from src.main.api.foundation.endpoint_senior import Endpoint
from src.main.api.foundation.requester.crud_requester_senior import CrudRequesterSenior
from src.main.api.foundation.requester.validator_crud_requester_senior import ValidateCrudRequesterSenior
from src.main.api.models.middle.login_user_request_middle import LoginUserRequestMiddle
from src.main.api.specs.request_specs_middle import RequestSpecs
from src.main.api.steps.base_steps_senior import BaseSteps
from src.main.api.specs.response_specs_middle import ResponseSpecs
from src.main.api.models.middle.create_user_request_middle import CreateUserRequestMiddle


class AdminSteps(BaseSteps):
    # Создание пользователя админом (Happy Path)
    def create_user(self, create_user_request_middle: CreateUserRequestMiddle):
        response = ValidateCrudRequesterSenior(
            # Именуем админские креды, так как у нового юзера прав на создание еще нет
            Endpoint.ADMIN_CREATE_USER,
            RequestSpecs.auth_admin_headers(username='admin', password='123456'),
            ResponseSpecs.request_ok()
        ).post(create_user_request_middle)
        # Сохраняем объект в сессию для автоматического удаления в teardown фикстуре
        self.created_obj.append(response)
        return response

    # Удаление пользователя админом по его id
    def delete_user(self, user_id: int):
        CrudRequesterSenior(
            Endpoint.ADMIN_DELETE_USER,
            RequestSpecs.auth_admin_headers(username='admin', password='123456'),
            ResponseSpecs.request_ok()
        ).delete(user_id)

    # Негативный сценарий создания (Проверка валидации полей)
    def create_invalid(self, create_user_request_middle: CreateUserRequestMiddle, expected_spec=None):
        # Если статус ошибки не передан, по умолчанию ожидаем 400 Bad Request
        response_spec = expected_spec if expected_spec is not None else ResponseSpecs.request_bad()
        CrudRequesterSenior(
            Endpoint.ADMIN_CREATE_USER,
            RequestSpecs.auth_admin_headers(username='admin', password='123456'),
            response_spec
        ).post(create_user_request_middle)

    # Авторизация пользователя в системе
    def login_user(self, login_user_request_middle: LoginUserRequestMiddle):
        response = ValidateCrudRequesterSenior(
            # Используем пустые заголовки, так как токена у юзера на момент логина еще нет
            Endpoint.LOGIN_USER,
            RequestSpecs.unauth_headers(),
            ResponseSpecs.request_ok()
        ).post(login_user_request_middle)

        return response





