import requests
import pytest
import allure

@pytest.mark.api

class TestDepositAccount():
    url = "http://localhost:4111"
    def test_bank_account_deposit_valid(self,user_with_accounts):
        deposit_amount = 1001.2
        token = user_with_accounts['token_user']
        account_id1 = user_with_accounts['account_1']

        with allure.step('1. Пополняем счет'):
            popolnenie_deposit_account = requests.post(
                url=f'{self.url}/api/account/deposit',
                json={
                    "accountId": account_id1,
                    "amount": deposit_amount
                },
                headers={
                    'accept': 'application/json',
                    'Authorization': f"Bearer {token}"
                }
            )

            print("\nТЕКСТ ОШИБКИ БЭКЕНДА:", popolnenie_deposit_account.text)

            allure.attach(
                body=popolnenie_deposit_account.text,  # Что прикрепляем (текст ответа)
                name="Ответ сервера (ожидается статус-код 200)",  # Как это будет называться в отчете
                attachment_type=allure.attachment_type.JSON  # Говорим Allure красиво подсветить JSON
            )

            # проверяем, пополнился ли счет на сумму пополнения
            assert popolnenie_deposit_account.status_code == 200
            assert popolnenie_deposit_account.json()['balance'] == deposit_amount


    # негативный тест на пополнение счета, где у нас нет токена авторизации
    def test_bank_account_deposit_invalid(self):
        with allure.step('1. Пополняем счет (негативный тест)'):
            bank_account_deposit_invalid = requests.post(
                url= f'{self.url}/api/account/deposit',
                json = {
                    "accountId": 2,
                    "amount": 1000.5
                },
                headers={
                    'accept': 'application/json'
                }
            )

            allure.attach(
                body=bank_account_deposit_invalid.text,  # Что прикрепляем (текст ответа)
                name="Ответ сервера (ожидается статус-код 401)",  # Как это будет называться в отчете
                attachment_type=allure.attachment_type.JSON  # Говорим Allure красиво подсветить JSON
            )
            print(bank_account_deposit_invalid.text)
            assert bank_account_deposit_invalid.status_code == 401
