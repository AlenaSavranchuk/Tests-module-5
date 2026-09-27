from dataclasses import dataclass
from enum import Enum
from src.main.api.models.mentor.base_model import BaseModel
from typing import Optional, Type
from src.main.api.models.mentor.create_user_request import CreateUserRequest
from src.main.api.models.mentor.create_user_response import CreateUserResponse
from src.main.api.models.mentor.login_user_request import LoginUserRequest
from src.main.api.models.mentor.login_user_response import LoginUserResponse
from src.main.api.models.mentor.create_account_response import CreateAccountResponse

# Объединяет URL, реквест и респонс модели каждой ручки в одном месте.
# Позволяет избежать дублирования строк и хардкода в тестах:
# методы запросов берут все настройки ручки из одного объекта конфигурации.

# Этот файл является "картой" всего API (API Registry). Он собирает в одном месте
# конфигурацию всех ручек (endpoints): их адреса, а также схемы запросов и ответов.

# Декоратор превращает класс в структуру данных с автоматически созданными методами сравнения и вывода.
@dataclass
class EndpointConfiguration:
    # Относительный путь к ручке API (например, '/admin/create').
    url: str
    # Ожидаемый тип Pydantic-модели для тела запроса (Type указывает, что мы передаем сам класс, а не его объект).
    request_model: Optional[Type[BaseModel]]
    # Ожидаемый тип Pydantic-модели для валидации ответа сервера.
    response_model: Optional[Type[BaseModel]]


# Перечисление (Enum) объединяет все ручки системы и позволяет удобно обращаться к их конфигурации через .value.
class Endpoint(Enum):

    # Конфигурация для ручки создания пользователя администратором.
    ADMIN_CREATE_USER = EndpointConfiguration(
        request_model = CreateUserRequest,
        url = '/admin/create',
        response_model = CreateUserResponse
    )

    # Конфигурация для ручки удаления пользователя администратором (модели пустые, так как ID передается в URL).
    ADMIN_DELETE_USER = EndpointConfiguration(
        request_model = None,
        url = '/admin/users',
        response_model = None
    )

    # Конфигурация для ручки авторизации пользователя в системе.
    LOGIN_USER = EndpointConfiguration(
        request_model = LoginUserRequest,
        url ='/auth/token/login',
        response_model = LoginUserResponse
    )

    # Конфигурация для ручки создания нового аккаунта.
    CREATE_ACCOUNT = EndpointConfiguration(
        request_model = None,
        url = '/account/create',
        response_model = CreateAccountResponse
    )
