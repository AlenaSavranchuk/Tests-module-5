import requests
import pytest
import allure
from src.main.api.specs.request_specs_middle import RequestSpecs
from src.main.api.models.middle.popolnenie_deposit_account_request import PopolnenieDepositAccountRequestMidlle
from src.main.api.requests.requesters_middle.popolnenie_deposit_requester_middle import PopolnenieDepositRequesterMiddle
from src.main.api.specs.response_specs_middle import ResponseSpecs


@pytest.mark.api
@pytest.mark.middle

class TestDepositAccount():
    def test_bank_account_deposit_valid(self,user_with_accounts):
        token = user_with_accounts['token_user']
        account_id1 = user_with_accounts['account_1']

        # Настраиваем спецификацию запроса: генерируем базовые заголовки и добавляем токен авторизации
        user_spec = RequestSpecs.unauth_headers()
        user_spec['headers']['Authorization'] = f"Bearer {token}"

        with allure.step('1. Пополняем счет'):
            popolnenie_deposit_account =PopolnenieDepositAccountRequestMidlle(
                accountId = account_id1,
                amount = 9000
            )

            popolnenie_deposit_account = PopolnenieDepositRequesterMiddle(
                request_speck_middle=user_spec,
                response_speck_middle=ResponseSpecs.request_ok(),
            ).post(popolnenie_deposit_account)

            allure.attach(
                body=popolnenie_deposit_account.model_dump_json(),  # Что прикрепляем (текст ответа)
                name="Ответ сервера (ожидается статус-код 200)",  # Как это будет называться в отчете
                attachment_type=allure.attachment_type.JSON  # Говорим Allure красиво подсветить JSON
            )


    # негативный тест на пополнение счета, где у нас нет токена авторизации
    def test_bank_account_deposit_invalid(self,user_with_accounts):
        token = user_with_accounts['token_user']
        account_id1 = user_with_accounts['account_1']

        # Настраиваем спецификацию запроса: генерируем базовые заголовки и добавляем токен авторизации
        user_spec = RequestSpecs.unauth_headers()

        with allure.step('1. Пополняем счет (негативный тест)'):
            bank_account_deposit_invalid = PopolnenieDepositAccountRequestMidlle(
                accountId = account_id1,
                amount = 9000
            )

            pop = PopolnenieDepositRequesterMiddle(
                request_speck_middle=user_spec,
                response_speck_middle=ResponseSpecs.request_unauthorized(),
            ).post(bank_account_deposit_invalid)

            allure.attach(
                body=pop.text,  # Что прикрепляем (текст ответа)
                name="Ответ сервера (ожидается статус-код 401)",  # Как это будет называться в отчете
                attachment_type=allure.attachment_type.JSON  # Говорим Allure красиво подсветить JSON
            )

