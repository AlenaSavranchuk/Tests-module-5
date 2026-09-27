import requests
import pytest
import allure
from sqlalchemy.orm import Session
from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.generators.data_generator import DataGenerator

@pytest.mark.api

class TestTransfer:
    url = "http://localhost:4111"
    def test_transfer_junior_valid(self,user_with_accounts: dict, db_session: Session):
        token_user = user_with_accounts["token_user"]
        account_id1 = user_with_accounts["account_1"]
        account_id2 = user_with_accounts["account_2"]
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
            assert popolnenie_deposit_account.json()['balance'] == test_data['deposit_amount']

        with allure.step('2. Переводим деньги на счет'):
            transfer_between_accounts = requests.post(
                url=f'{self.url}/api/account/transfer',
                json={
                    "fromAccountId": account_id1,
                    "toAccountId": account_id2,
                    "amount": test_data['deposit_amount']
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
            assert transfer_between_accounts.json().get('fromAccountIdBalance') == 0

            account_1_db = AccountCrudDb.get_account_by_id(db_session, account_id1)
            account_2_db = AccountCrudDb.get_account_by_id(db_session, account_id2)
            assert account_1_db.balance == 0


# негативный тест на этот же тест-кейс (без пополнения переводим, то есть,переводить нечего)
    def test_transfer_junior_invalid(self,user_with_accounts: dict, db_session: Session):
        with allure.step('1. Пополнение счета'):
            test_data = DataGenerator.get_credit_data()
            token_user = user_with_accounts["token_user"]
            account_id1 = user_with_accounts["account_1"]
            account_id2 = user_with_accounts["account_2"]

            account_1_before = AccountCrudDb.get_account_by_id(db_session, account_id1)
            account_2_before = AccountCrudDb.get_account_by_id(db_session, account_id2)

            balance_1_before = account_1_before.balance if account_1_before else 0
            balance_2_before = account_2_before.balance if account_2_before else 0

            with allure.step('Переводим деньги на счет'):
                transfer_between_accounts = requests.post(
                url = f'{self.url}/api/account/transfer',
                json = {
                    "fromAccountId": account_id1,
                    "toAccountId": account_id2,
                    "amount": test_data['deposit_amount']
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

            account_1_after = AccountCrudDb.get_account_by_id(db_session, account_id1)
            account_2_after = AccountCrudDb.get_account_by_id(db_session, account_id2)

            balance_1_after = account_1_after.balance if account_1_after else 0
            balance_2_after = account_2_after.balance if account_2_after else 0

            # Проверяем, что баланс отправителя не изменился
            assert balance_1_after == balance_1_before

            # Проверяем, что баланс получателя не изменился
            assert balance_2_after == balance_2_before