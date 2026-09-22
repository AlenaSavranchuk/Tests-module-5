import requests
import pytest
import allure

@pytest.mark.api

class TestTransfer():
    url = "http://localhost:4111"
    def test_transfer_junior_valid(self,user_with_accounts):

        token_user = user_with_accounts["token_user"]
        account_id1 = user_with_accounts["account_1"]
        account_id2 = user_with_accounts["account_2"]

        deposit_amount = 1000.0
        transfer_amount = 500.75

        with allure.step('1. Пополняем счет'):
            popolnenie_deposit_account = requests.post(
                url=f'{self.url}/api/account/deposit',
                json={
                    "accountId": account_id1,
                    "amount": deposit_amount
                },
                headers={
                    'accept': 'application/json',
                    'Authorization': f"Bearer {token_user}"
                }
            )

            allure.attach(
                body=popolnenie_deposit_account.text,  # Что прикрепляем (текст ответа)
                name="Ответ сервера (ожидается статус-код 200)",  # Как это будет называться в отчете
                attachment_type=allure.attachment_type.JSON  # Говорим Allure красиво подсветить JSON
            )

            # проверяем, пополнился ли счет на сумму пополнения
            assert popolnenie_deposit_account.status_code == 200
            assert popolnenie_deposit_account.json()['balance'] == deposit_amount

        with allure.step('2. Переводим деньги на счет'):
            transfer_between_accounts = requests.post(
                url=f'{self.url}/api/account/transfer',
                json={
                    "fromAccountId": account_id1,
                    "toAccountId": account_id2,
                    "amount": transfer_amount
                },
                headers={
                    'accept': 'application/json',
                    'Authorization': f"Bearer {token_user}"
                }
            )

            allure.attach(
                body=transfer_between_accounts.text,  # Что прикрепляем (текст ответа)
                name="Ответ сервера (ожидается статус-код 200)",  # Как это будет называться в отчете
                attachment_type=allure.attachment_type.JSON  # Говорим Allure красиво подсветить JSON
            )

            assert transfer_between_accounts.status_code == 200
            assert transfer_between_accounts.json().get('fromAccountIdBalance') == deposit_amount - transfer_amount


# негативный тест на этот же тест-кейс
    def test_transfer_junior_invalid(self,user_with_accounts):
        with allure.step('1. Пополнение счета'):
            token_user = user_with_accounts["token_user"]
            account_id1 = user_with_accounts["account_1"]
            account_id2 = user_with_accounts["account_2"]

            deposit_amount = 0
            transfer_amount = 500

            transfer_between_accounts = requests.post(
                url = f'{self.url}/api/account/transfer',
                json = {
                    "fromAccountId": account_id1,
                    "toAccountId": account_id2,
                    "amount": 500
                },
                headers = {
                    'accept': 'application/json',
                    'Authorization': f"Bearer {token_user}"
                }
                )

            allure.attach(
                body=transfer_between_accounts.text,  # Что прикрепляем (текст ответа)
                name="Ответ сервера (ожидается статус-код 422)",  # Как это будет называться в отчете
                attachment_type=allure.attachment_type.JSON  # Говорим Allure красиво подсветить JSON
            )

            assert transfer_between_accounts.status_code == 422
            assert transfer_between_accounts.json().get('error') is not None
