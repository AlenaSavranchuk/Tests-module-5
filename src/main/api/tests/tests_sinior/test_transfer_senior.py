import pytest
import allure
from sqlalchemy.orm import Session
from src.main.api.generators.data_generator import DataGenerator
from src.main.api.clasess.api_manager_senior import ApiManagerSenior
from src.main.api.db.crud.transaction_crud import TransactionCrud
from src.main.api.fixtures.db_fixture import db_session
from src.main.api.foundation.endpoint_senior import Endpoint
from src.main.api.db.models.account_table import Account
from src.main.api.specs.response_specs_middle import ResponseSpecs
from src.main.api.models.middle.transfer_request_middle import TransferRequestMiddle

@pytest.mark.api
@pytest.mark.senior

class TestTransfer:
    def test_transfer_senior_valid(self,api_client: ApiManagerSenior, standart_role_plus_accounts_popolnenie: dict, db_session: Session):
        api_client.user_steps.authorize(standart_role_plus_accounts_popolnenie['token_user'])
        test_data = DataGenerator.get_credit_data()

        with allure.step('Перевод со счета на счет'):
            transfer_request = TransferRequestMiddle(
                fromAccountId=standart_role_plus_accounts_popolnenie['account_1'],
                toAccountId=standart_role_plus_accounts_popolnenie['account_2'],
                amount=test_data['deposit_amount']
            )

            balance_before = db_session.query(Account.balance).filter_by(
                id=standart_role_plus_accounts_popolnenie['account_1']).scalar()
            transfer_response = api_client.user_steps.transfer_credit(transfer_request_middle=transfer_request)

            expected_balance = balance_before - transfer_request.amount
            assert transfer_response.fromAccountIdBalance == expected_balance

            transfer_from_db = TransactionCrud.get_transaction_account(db_session, transfer_request.fromAccountId,transfer_request.toAccountId)
            assert transfer_from_db is not None
            assert transfer_from_db.from_account_id == transfer_response.fromAccountId
            assert transfer_from_db.to_account_id == transfer_response.toAccountId


        # негативный тест на этот же тест-кейс
    def test_transfer_senior_invalid(self, api_client: ApiManagerSenior, user_fixture_senior: dict, db_session: Session, standart_role_plus_accounts_popolnenie:dict):
        api_client.user_steps.authorize(standart_role_plus_accounts_popolnenie['token_user'])
        test_data = DataGenerator.get_credit_data()

        with allure.step('Перевод средств'):
            transfer_request = TransferRequestMiddle(
                fromAccountId=56,
                toAccountId=25,
                amount=test_data['deposit_amount']
            )

            api_client.user_steps.execute_negative_request(
                endpoint=Endpoint.TRANSFER_ACCOUNT,
                model=transfer_request,
                expected_spec=ResponseSpecs.request_not_found()
            )

            transfer_from_db_invalid = TransactionCrud.get_transaction_id(db_session, transfer_request.toAccountId)
            assert transfer_from_db_invalid is None
