import requests
import pytest
import allure
from src.main.api.specs.request_specs_middle import RequestSpecs
from src.main.api.models.middle.popolnenie_deposit_account_request import PopolnenieDepositAccountRequestMidlle
from src.main.api.requests.requesters_middle.popolnenie_deposit_requester_middle import PopolnenieDepositRequesterMiddle
from src.main.api.specs.response_specs_middle import ResponseSpecs
from src.main.api.models.middle.transfer_request_middle import TransferRequestMiddle
from src.main.api.requests.requesters_middle.transfer_requester_middle import TransferRequesterMiddle
@pytest.mark.api
@pytest.mark.middle

class TestTransfer():
    url = "http://localhost:4111"
    def test_transfer_middle_valid(self,user_with_accounts):

        token = user_with_accounts['token_user']
        account_id1 = user_with_accounts['account_1']
        account_id2 = user_with_accounts['account_2']

        # Настраиваем спецификацию запроса: генерируем базовые заголовки и добавляем токен авторизации
        user_spec = RequestSpecs.unauth_headers()
        user_spec['headers']['Authorization'] = f"Bearer {token}"

        with allure.step('1. Пополняем счет'):
            popolnenie_deposit_account = PopolnenieDepositAccountRequestMidlle(
                accountId = account_id1,
                amount = 9000
            )

            response_pop = PopolnenieDepositRequesterMiddle(
                request_speck_middle=user_spec,
                response_speck_middle=ResponseSpecs.request_ok(),
            ).post(popolnenie_deposit_account)

            allure.attach(
                body=popolnenie_deposit_account.model_dump_json(),  # Что прикрепляем (текст ответа)
                name="Ответ сервера (ожидается статус-код 200)",  # Как это будет называться в отчете
                attachment_type=allure.attachment_type.JSON  # Говорим Allure красиво подсветить JSON
            )

            with allure.step('2. Переводим со счета 1 на счет 2'):
                transfer_accounts = TransferRequestMiddle(
                    fromAccountId = account_id1,
                    toAccountId = account_id2,
                    amount = 1000
                )

            transfer_accounts_response = TransferRequesterMiddle(
                request_speck_middle=user_spec,
                response_speck_middle=ResponseSpecs.request_ok(),
            ).post(transfer_accounts)

            allure.attach(
                body=transfer_accounts_response.model_dump_json(),  # Что прикрепляем (текст ответа)
                name="Ответ сервера (ожидается статус-код 200)",  # Как это будет называться в отчете
                attachment_type=allure.attachment_type.JSON  # Говорим Allure красиво подсветить JSON
            )



        # негативный тест на этот же тест-кейс
    def test_transfer_middle_invalid(self,user_with_accounts):
        with allure.step('1. Пополнение счета'):
            token_user = user_with_accounts["token_user"]
            account_id1 = user_with_accounts["account_1"]
            account_id2 = user_with_accounts["account_2"]

            user_spec = RequestSpecs.unauth_headers()

            with allure.step('1. Переводим со счета 1 на счет 2'):
                transfer_accounts = TransferRequestMiddle(
                    fromAccountId=account_id1,
                    toAccountId=account_id2,
                    amount=1000
                )

            transfer_accounts_response = TransferRequesterMiddle(
                request_speck_middle=user_spec,
                response_speck_middle=ResponseSpecs.request_unauthorized(),
            ).post(transfer_accounts)

            allure.attach(
                body=transfer_accounts_response.text,  # Что прикрепляем (текст ответа)
                name="Ответ сервера (ожидается статус-код 401)",  # Как это будет называться в отчете
                attachment_type=allure.attachment_type.JSON
            )# Говорим Allure красиво подсветить JSON
