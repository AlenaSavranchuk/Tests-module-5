import pytest
import allure
from sqlalchemy.orm import Session
from src.main.api.clasess.api_manager_senior import ApiManagerSenior
from src.main.api.fixtures.api_fixture_senior import api_client
from src.main.api.fixtures.db_fixture import db_session
from src.main.api.foundation.endpoint_senior import Endpoint
from src.main.api.models.middle.popolnenie_deposit_account_request import PopolnenieDepositAccountRequestMidlle
from src.main.api.generators.data_generator import DataGenerator
from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.db.crud.transaction_crud import TransactionCrud
from src.main.api.specs.response_specs_middle import ResponseSpecs


@pytest.mark.api
@pytest.mark.senior
class TestDepositAccount:
    def test_bank_account_deposit_valid(self, api_client: ApiManagerSenior, user_with_accounts: dict, db_session: Session):
        test_data = DataGenerator.get_credit_data()
        account_data = user_with_accounts["account_1"]
        balance_before = AccountCrudDb.get_account_balance(db_session, account_data)

        with allure.step('Пополнение счета'):
            deposit_account = PopolnenieDepositAccountRequestMidlle(
                accountId=account_data,
                amount=test_data['deposit_amount']
            )

            deposit_response = api_client.user_steps.popolnenie_account(popolnenie_deposit_account_request=deposit_account)

            assert deposit_response.balance == balance_before + deposit_account.amount
            assert deposit_response.id ==  account_data

            # проверяем сумму пополнения
            deposit_from_db = TransactionCrud.get_transaction_id(db_session, deposit_account.accountId)
            assert deposit_from_db is not None
            assert deposit_from_db.amount == deposit_account.amount

    # негативный тест на пополнение счета, где у нас нет токена авторизации
    def test_bank_account_deposit_invalid(self,api_client: ApiManagerSenior, user_with_accounts: dict, db_session: Session):
        test_data = DataGenerator.get_credit_data()
        account_data = user_with_accounts["account_1"]

        with allure.step('Пополнение счета'):
            deposit_account = PopolnenieDepositAccountRequestMidlle(
                accountId=account_data,
                amount=test_data['deposit_amount']
            )

            api_client.user_steps.execute_negative_request(
                endpoint=Endpoint.POPOLNENIE_ACCOUNT,
                model=deposit_account,
                expected_spec=ResponseSpecs.request_unauthorized(),
            )

        deposit_from_db = TransactionCrud.get_transaction_id(db_session,deposit_account.accountId)
        assert deposit_from_db is None, f'Ошибка:в базе обнаружен {deposit_from_db}'

