import requests
import pytest
import uuid
import allure

@pytest.mark.api

class TestCreditRequest:
    url = "http://localhost:4111"
# функция на кредитик с фикстурой,у которой секретная роль для юзера
    def test_credit_request_valid(self,secret_credit_user_with_accounts):
        token_user = secret_credit_user_with_accounts ['token_user']
        account_2 = secret_credit_user_with_accounts['account_2']
        with allure.step('1. Запрос на кредит'):
            credit_request = requests.post(
                url = f'{self.url}/api/credit/request',
                json = {
                    "accountId": account_2,
                    "amount": 5000,
                    "termMonths": 12
                },
                headers = {
                    "Content-Type": "application/json",
                    "accept": "application/json",
                    "Authorization":f"Bearer {token_user}"
                }

            )

            allure.attach(
                body=credit_request.text,  # Что прикрепляем (текст ответа)
                name="Ответ сервера (ожидается статус-код 201)",  # Как это будет называться в отчете
                attachment_type=allure.attachment_type.JSON  # Говорим Allure красиво подсветить JSON
            )
        assert credit_request.status_code == 201

# негативный тест на запрос получения кредита на тот же счет, что я уже взяла для первого кредита
    def test_credit_request_invalid(self,secret_credit_user_with_accounts):
        token_user = secret_credit_user_with_accounts['token_user']
        account_1 = secret_credit_user_with_accounts['account_1']
        with allure.step('1. Запрос на кредит'):
            credit_request_new = requests.post(
                url = f'{self.url}/api/credit/request',
                json = {
                    "accountId": account_1,
                    "amount": 5000,
                    "termMonths": 12
                },
                headers = {
                    "Content-Type": "application/json",
                    "accept": "application/json",
                    "Authorization":f"Bearer {token_user}"
                }

            )

            allure.attach(
                body=credit_request_new.text,  # Что прикрепляем (текст ответа)
                name="Ответ сервера (ожидается статус-код 201))",  # Как это будет называться в отчете
                attachment_type=allure.attachment_type.JSON  # Говорим Allure красиво подсветить JSON
            )

            assert credit_request_new.status_code == 201

        with allure.step('2. Запрос на второй кредит'):
            credit_request_new2 = requests.post(
                url=f'{self.url}/api/credit/request',
                json={
                    "accountId": account_1,
                    "amount": 5000,
                    "termMonths": 12
                },
                headers={
                    "Content-Type": "application/json",
                    "accept": "application/json",
                    "Authorization": f"Bearer {token_user}"
                }

            )

            allure.attach(
                body=credit_request_new2.text,  # Что прикрепляем (текст ответа)
                name="Ответ сервера (ожидается статус-код 404)",  # Как это будет называться в отчете
                attachment_type=allure.attachment_type.JSON  # Говорим Allure красиво подсветить JSON
            )

            assert credit_request_new2.status_code == 404

