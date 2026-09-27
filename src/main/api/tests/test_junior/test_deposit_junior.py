import requests
import pytest
import allure
from sqlalchemy.orm import Session
from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.generators.data_generator import DataGenerator

@pytest.mark.api

class TestDepositAccount():
    url = "http://localhost:4111"
    def test_bank_account_deposit_valid(self,user_with_accounts: dict, db_session: Session):
        token = user_with_accounts['token_user']
        account_id1 = user_with_accounts['account_1']
        test_data = DataGenerator.get_credit_data()

        with allure.step('1. Пополняем счет'):
            popolnenie_deposit_account = requests.post(
                url=f'{self.url}/api/account/deposit',
                json={
                    "accountId": account_id1,
                    "amount": test_data['deposit_amount']
                },
                headers={
                    'accept': 'application/json',
                    'Authorization': f"Bearer {token}"
                }
            )

            allure.attach(
                body=popolnenie_deposit_account.text,  # Что прикрепляем (текст ответа)
                name="Ответ сервера (ожидается статус-код 200)",  # Как это будет называться в отчете
                attachment_type=allure.attachment_type.JSON  # Говорим Allure красиво подсветить JSON
            )

            # проверяем, пополнился ли счет на сумму пополнения
            assert popolnenie_deposit_account.status_code == 200
            assert popolnenie_deposit_account.json()['balance'] == test_data['deposit_amount']

            account_db = AccountCrudDb.get_account_by_id(db_session, account_id1)
            assert account_db is not None, f"Аккаунт с ID {account_id1} не найден в базе данных"


    # негативный тест на пополнение счета, где у нас нет токена авторизации
    def test_bank_account_deposit_invalid(self, db_session: Session):
        test_data = DataGenerator.get_credit_data()
        account_id = 2
        account_before = AccountCrudDb.get_account_by_id(db_session, account_id)
        balance_before = account_before.balance if account_before else 0

        with allure.step('1. Пополняем счет (негативный тест)'):
            bank_account_deposit_invalid = requests.post(
                url= f'{self.url}/api/account/deposit',
                json = {
                    "accountId": account_id,
                    "amount": test_data['deposit_amount']
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

            account_after = AccountCrudDb.get_account_by_id(db_session, account_id)
            balance_after = account_after.balance if account_after else 0

            assert bank_account_deposit_invalid.status_code == 401
            assert balance_after == balance_before, f"Баланс был: {balance_before}, стал: {balance_after}"
