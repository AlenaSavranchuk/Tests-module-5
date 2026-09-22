from dataclasses import dataclass
from enum import Enum
from typing import Optional, Type
from pydantic import BaseModel
from src.main.api.models.middle.credit_repay_request_middle import CreditRepayRequestMiddle
from src.main.api.models.middle.create_account_response_middle import CreateAccountResponseMiddle
from src.main.api.models.middle.create_user_request_middle import CreateUserRequestMiddle
from src.main.api.models.middle.create_user_response_middle import CreateUserResponseMiddle
from src.main.api.models.middle.credit_repay_response_middle import CreditRepayResponseMiddle
from src.main.api.models.middle.credit_request_middle import CreditRequestMiddle
from src.main.api.models.middle.credit_response_middle import CreditResponseMiddle
from src.main.api.models.middle.login_user_request_middle import LoginUserRequestMiddle
from src.main.api.models.middle.login_user_response_middle import LoginUserResponseMiddle
from src.main.api.models.middle.popolnenie_deposit_account_request import PopolnenieDepositAccountRequestMidlle
from src.main.api.models.middle.popolnenie_deposit_account_response import PopolnenieDepositAccountResponseMiddle
from src.main.api.models.middle.transfer_request_middle import TransferRequestMiddle
from src.main.api.models.middle.transfer_response_middle import TransferResponseMiddle
# Объединяет URL, реквест и респонс модели каждой ручки в одном месте.
# Позволяет избежать дублирования строк и хардкода в тестах:
# методы запросов берут все настройки ручки из одного объекта конфигурации.

# Этот файл является "картой" всего API (API Registry). Он собирает в одном месте
# конфигурацию всех ручек (endpoints): их адреса, а также схемы запросов и ответов.

@dataclass
class EndpointConfigurationSenior:
    url: str
    request_model: Optional[Type[BaseModel]]
    response_model: Optional[Type[BaseModel]]

class Endpoint(Enum):
    # Конфигурация для ручки создания пользователя администратором
    ADMIN_CREATE_USER = EndpointConfigurationSenior(
        request_model=CreateUserRequestMiddle,
        url='/admin/create',
        response_model=CreateUserResponseMiddle
    )

    # Конфигурация для ручки авторизации пользователя в системе
    LOGIN_USER = EndpointConfigurationSenior(
        request_model=LoginUserRequestMiddle,
        url='/auth/token/login',
        response_model=LoginUserResponseMiddle
    )

    # Создание банковского счета
    CREATE_DEPOSIT_ACCOUNT = EndpointConfigurationSenior(
        request_model= None,
        url='/account/create',
        response_model=CreateAccountResponseMiddle
    )

    # Конфигурация для ручки удаления пользователя администратором (модели пустые, так как ID передается в URL).
    ADMIN_DELETE_USER = EndpointConfigurationSenior(
        request_model=None,
        url='/admin/users',
        response_model=None
    )

    # Пополнение счета
    POPOLNENIE_ACCOUNT = EndpointConfigurationSenior(
        request_model=PopolnenieDepositAccountRequestMidlle,
        url='/account/deposit',
        response_model=PopolnenieDepositAccountResponseMiddle
    )

    # Перевод между счетами
    TRANSFER_ACCOUNT = EndpointConfigurationSenior(
        request_model=TransferRequestMiddle,
        url='/account/transfer',
        response_model=TransferResponseMiddle
    )

    # Запрос на получение кредита
    CREDIT_REQUEST = EndpointConfigurationSenior(
        request_model=CreditRequestMiddle,
        url='/credit/request',
        response_model=CreditResponseMiddle
    )

    # Погашение кредита
    CREDIT_REPAY = EndpointConfigurationSenior(
        request_model=CreditRepayRequestMiddle,
        url='/credit/repay',
        response_model=CreditRepayResponseMiddle
    )


