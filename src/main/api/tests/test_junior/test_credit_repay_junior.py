import requests
import pytest
from sqlalchemy.orm import Session
from src.main.api.db.crud.credit_crud import CreditCrudDb
from src.main.api.generators.data_generator import DataGenerator


@pytest.mark.api

class TestCreditRepay:
    def test_credit_repay(self, secret_credit_user_with_accounts: dict, db_session: Session):
            # сначала создаем кредит
            base_url = "http://localhost:4111/api"
            test_data = DataGenerator.get_credit_data()
            token_user = secret_credit_user_with_accounts['token_user']
            account_1 = secret_credit_user_with_accounts['account_1']
            credit_request = requests.post(
                url=f'{base_url}/credit/request',
                json={
                    "accountId": account_1,
                    "amount": test_data['credit_amount'],
                    "termMonths": test_data['term_months']
                },
                headers={
                    "Content-Type": "application/json",
                    "accept": "application/json",
                    "Authorization": f"Bearer {token_user}"
                }

            )

            assert credit_request.status_code == 201
            credit_id = int(credit_request.json()['creditId'])


            # пополняем счет
            popolnenie_deposit_account = requests.post(
                url=f'{base_url}/account/deposit',
                json={
                    "accountId": account_1,
                    "amount": test_data['credit_amount'],
                },
                headers={
                    'accept': 'application/json',
                    'Authorization': f"Bearer {token_user}"
                }
            )

            # проверяем, пополнился ли счет на сумму пополнения
            assert popolnenie_deposit_account.status_code == 200


            # создаем запрос на погашение самого кредита
            credit_repay_request = requests.post(
                url=f'{base_url}/credit/repay',
                json={
                    "creditId": credit_id,
                    "accountId": account_1,
                    "amount": test_data['credit_amount'],
                },
                headers={
                    "Content-Type": "application/json",
                    "accept": "application/json",
                    "Authorization": f"Bearer {token_user}"
                }
            )

            assert credit_request.status_code == 201, 'Ошибка: вернулся некорректный статус-код при создании кредита'

            credit_repay_db = CreditCrudDb.get_credit_id(db_session, credit_id)
            assert credit_repay_db.balance == 0, 'Ошибка: баланс кредита в базе данных не равен нулю'

    # для негативного теста, тут не хватает денег
    def test_credit_request_invalid(self, secret_credit_user_with_accounts: dict, db_session: Session):
            test_data = DataGenerator.get_credit_data()
            base_url = "http://localhost:4111/api"
            token_user = secret_credit_user_with_accounts['token_user']
            account_1 = secret_credit_user_with_accounts['account_1']
            credit_request_invalid = requests.post(
                url=f'{base_url}/credit/request',
                json={
                    "accountId": account_1,
                    "amount": test_data['credit_amount'],
                    "termMonths": test_data['term_months']
                },
                headers={
                    "Content-Type": "application/json",
                    "accept": "application/json",
                    "Authorization": f"Bearer {token_user}"
                }

            )

            assert credit_request_invalid.status_code == 201
            credit_id = credit_request_invalid.json()['creditId']

            # создаем запрос на погашение самого кредита
            credit_repay_request_invalid2 = requests.post(
                url=f'{base_url}/credit/repay',
                json={
                    "creditId": credit_id,
                    "accountId": account_1,
                    "amount": test_data['credit_amount']*1000,
                },
                headers={
                    "Content-Type": "application/json",
                    "accept": "application/json",
                    "Authorization": f"Bearer {token_user}"
                }
            )

            assert credit_repay_request_invalid2.status_code == 422, 'Ошибка: вернулся некорректный статус-код при отправке невалидного запроса'

            credit_db = CreditCrudDb.get_credit_id(db_session, credit_id)
            assert credit_db.balance == - test_data['credit_amount'], 'Ошибка: баланс кредита в базе данных изменился после неуспешного запроса'



