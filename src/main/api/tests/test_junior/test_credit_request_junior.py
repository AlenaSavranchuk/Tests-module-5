import requests
import pytest
from sqlalchemy.orm import Session
from src.main.api.db.crud.credit_crud import CreditCrudDb
from src.main.api.generators.data_generator import DataGenerator
import allure

@pytest.mark.api

class TestCreditRequest:
    def test_credit_request_valid(self,secret_credit_user_with_accounts: dict, db_session: Session):
        url = "http://localhost:4111"
        token_user = secret_credit_user_with_accounts ['token_user']
        account_2 = secret_credit_user_with_accounts['account_2']
        test_data = DataGenerator.get_credit_data()

        with allure.step('1. Запрос на кредит'):
            credit_request = requests.post(
                url = f'{url}/api/credit/request',
                json = {
                    "accountId": account_2,
                    "amount": test_data['credit_amount'],
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

        credit_id = int(credit_request.json()['creditId'])
        credit_db = CreditCrudDb.get_credit_id(db_session, credit_id)
        assert credit_db is not None, f"Кредит с ID {credit_id} не найден в базе данных"


# негативный тест на запрос получения кредита на тот же счет, что я уже взяла для первого кредита
    def test_credit_request_invalid(self,secret_credit_user_with_accounts: dict, db_session: Session):
        token_user = secret_credit_user_with_accounts['token_user']
        account_1 = secret_credit_user_with_accounts['account_1']
        test_data = DataGenerator.get_credit_data()
        url = "http://localhost:4111"

        with allure.step('1. Запрос на кредит'):
            credit_request_new = requests.post(
                url = f'{url}/api/credit/request',
                json = {
                    "accountId": account_1,
                    "amount": test_data['credit_amount'],
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
            first_credit_id = int(credit_request_new.json()['creditId'])

        with allure.step('2. Запрос на второй кредит'):
            credit_request_new2 = requests.post(
                url=f'{url}/api/credit/request',
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

            first_credit_db = CreditCrudDb.get_credit_id(db_session, first_credit_id)
            assert first_credit_db is not None
            assert first_credit_db.balance == -test_data['credit_amount']
