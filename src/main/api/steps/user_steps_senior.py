# сложный файл
from src.main.api.foundation.endpoint_senior import Endpoint
from src.main.api.models.middle.credit_request_middle import CreditRequestMiddle
from src.main.api.models.middle.popolnenie_deposit_account_request import PopolnenieDepositAccountRequestMidlle
from src.main.api.models.middle.transfer_request_middle import TransferRequestMiddle
from src.main.api.specs.request_specs_middle import RequestSpecs
from src.main.api.specs.response_specs_middle import ResponseSpecs
from src.main.api.steps.base_steps_senior import BaseSteps
from src.main.api.foundation.requester.validator_crud_requester_senior import ValidateCrudRequesterSenior
from src.main.api.models.middle.create_user_request_middle import CreateUserRequestMiddle
from src.main.api.models.middle.credit_repay_request_middle import CreditRepayRequestMiddle
from pydantic import BaseModel
from typing import Any
from src.main.api.foundation.requester.crud_requester_senior import CrudRequesterSenior
class UserSteps(BaseSteps):

    # создаем банковский счет
    def create_deposit_account(self,create_user_request_middle: CreateUserRequestMiddle):
        user_spec = RequestSpecs.unauth_headers()
        user_spec['headers']['Authorization'] = f'Bearer {self.token}'
        response = ValidateCrudRequesterSenior(
            request_specs_middle = user_spec,
            endpoint=Endpoint.CREATE_DEPOSIT_ACCOUNT,
            response_specs_middle=ResponseSpecs.request_created()
        ).post(create_user_request_middle)

        self.created_obj.append(response)
        return response

    # пополняем счет
    def popolnenie_account(self,popolnenie_deposit_account_request: PopolnenieDepositAccountRequestMidlle):
        user_spec = RequestSpecs.unauth_headers()
        user_spec['headers']['Authorization'] = f'Bearer {self.token}'
        response = ValidateCrudRequesterSenior(
            request_specs_middle=user_spec,
            endpoint=Endpoint.POPOLNENIE_ACCOUNT,
            response_specs_middle=ResponseSpecs.request_ok()
        ).post(popolnenie_deposit_account_request)

        return response

    # выдача кредита
    def credit_account(self, credit_request_middle: CreditRequestMiddle):
        user_spec = RequestSpecs.unauth_headers()
        user_spec['headers']['Authorization'] = f'Bearer {self.token}'
        response = ValidateCrudRequesterSenior(
            request_specs_middle=user_spec,
            endpoint=Endpoint.CREDIT_REQUEST,
            response_specs_middle=ResponseSpecs.request_created()
        ).post(credit_request_middle)  # Физически отправляем POST-запрос с телом кредитной заявки на бэкенд.

        # ВНИМАНИЕ: Нам обязательно нужно добавить кредит в корзину для очистки перед return!
        # Так как кредит создает долговое обязательство в банковской базе данных, после теста его нужно снести.
        self.created_obj.append(response)

        # Возвращаем проверенную Pydantic-модель одобренного кредита обратно в тест.
        return response

    # перевод со счета на счет
    def transfer_credit(self, transfer_request_middle: TransferRequestMiddle):
        user_spec = RequestSpecs.unauth_headers()
        user_spec['headers']['Authorization'] = f'Bearer {self.token}'
        response = ValidateCrudRequesterSenior(
            request_specs_middle=user_spec,
            endpoint=Endpoint.TRANSFER_ACCOUNT,
            response_specs_middle=ResponseSpecs.request_ok()
        ).post(transfer_request_middle)  # Отправляем POST-запрос с заполненным телом перевода (откуда, куда, сколько).

        # Корзину очистки (self.created_obj.append) здесь не используем, так как операция только меняет баланс.
        return response

    # погашение кредита
    def credit_repay(self, credit_repay_request_middle: CreditRepayRequestMiddle):
        user_spec = RequestSpecs.unauth_headers()
        user_spec['headers']['Authorization'] = f'Bearer {self.token}'
        response = ValidateCrudRequesterSenior(
            request_specs_middle=user_spec,
            endpoint=Endpoint.CREDIT_REPAY,
            response_specs_middle=ResponseSpecs.request_ok()
        ).post(credit_repay_request_middle)  # Отправляем POST-запрос с заполненным телом погашения (сумма, ID кредита).

        # Корзину очистки не используем, так как эта операция уменьшает/закрывает долг, а не создает новый.
        return response

    def authorize(self, token: str, role: str = "user"):
        self.token = token
        self.role = role  # сохраняем роль, если она пригодится в заголовках

    # Универсальный метод для проверки любых негативных сценариев
    def execute_negative_request(self, endpoint: Any, model: BaseModel, expected_spec: Any):
        # 1. Берем неавторизованные заголовки
        user_spec = RequestSpecs.unauth_headers()
        # 2. Подставляем токен из нашего сейфа, чтобы бэк знал, кто делает запрос
        token = getattr(self, 'token', None)
        if token:
            user_spec['headers']['Authorization'] = f'Bearer {token}'
        # 3. Вызываем базовый реквестер и явно передаем все аргументы по именам
        CrudRequesterSenior(
            request_specs_middle=user_spec,
            endpoint=endpoint,
            response_specs_middle=expected_spec
        ).post(model)  # Отправляем нашу Pydantic-модель с ошибкой

