import pytest
from src.main.api.models.middle.credit_repay_request_middle import CreditRepayRequestMiddle
from src.main.api.specs.response_specs_middle import ResponseSpecs
from src.main.api.models.middle.popolnenie_deposit_account_request import PopolnenieDepositAccountRequestMidlle
from src.main.api.models.middle.credit_request_middle import CreditRequestMiddle
from src.main.api.foundation.endpoint_senior import Endpoint
import allure


@pytest.mark.api
@pytest.mark.senior
class TestCreditRepay:
    url = "http://localhost:4111"

    # позитивный тест
    def test_credit_repay(self, api_client, credit_request_fixture):
        response = api_client.admin_steps.login_user(credit_request_fixture)
        api_client.user_steps.authorize(response.token)

        with allure.step('ШАГ 1: Пополнение счета (Депозит)'):
            account_1 = api_client.user_steps.create_deposit_account(credit_request_fixture)
            deposit_data = PopolnenieDepositAccountRequestMidlle(
                accountId=account_1.id,
                amount=9000,
            )
            api_client.user_steps.popolnenie_account(popolnenie_deposit_account_request=deposit_data)

        with allure.step('ШАГ 2: Создание кредита'):
            credit_creation_data = CreditRequestMiddle(
                accountId=account_1.id,
                amount=5000,
                termMonths=11
            )
            # Отправляем запрос на создание кредита. Ждем статус 201 Created.
            response_credit = api_client.user_steps.credit_account(credit_request_middle=credit_creation_data)

        with allure.step('ШАГ 3:  Погашение кредита'):
            repay_data = CreditRepayRequestMiddle(
                creditId=response_credit.creditId,
                accountId=account_1.id,
                amount=5000,
            )
            api_client.user_steps.credit_repay(credit_repay_request_middle=repay_data)


    # негативный тест, когда невозможно взять 2 кредита на 1 счет
    def test_credit_request_invalid(self, api_client, credit_request_fixture) :
        response = api_client.admin_steps.login_user(credit_request_fixture)
        api_client.user_steps.authorize(response.token)

        with allure.step('ШАГ 3:  Создание кредита'):
            account_1 = api_client.user_steps.create_deposit_account(credit_request_fixture)
            credit_creation_data = CreditRequestMiddle(
                accountId=account_1.id,
                amount=5000,
                termMonths=11
            )
            # Отправляем запрос на создание кредита. Ждем статус 201 Created.
            response_credit = api_client.user_steps.credit_account(credit_request_middle=credit_creation_data)

        with allure.step('ШАГ 2: Попытка взять второй кредит на тот же счет '):
            credit_creation_data = CreditRequestMiddle(
                accountId=account_1.id,
                amount=5000,
                termMonths=11
            )

        # Вызываем УНИВЕРСАЛЬНЫЙ метод и говорим ему: "Жди ошибку 400 Bad Request!"
        api_client.user_steps.execute_negative_request(
            endpoint=Endpoint.CREDIT_REQUEST,
            model=credit_creation_data,
            expected_spec=ResponseSpecs.request_not_found()  # Указываем, что ждем ошибку от бэка
        )



