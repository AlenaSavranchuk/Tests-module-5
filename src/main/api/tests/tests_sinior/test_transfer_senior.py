import pytest
import allure
from sqlalchemy.orm import Session
from src.main.api.db.crud.transaction_crud import TransactionCrud
from src.main.api.fixtures.db_fixture import db_session
from src.main.api.foundation.endpoint_senior import Endpoint
from src.main.api.models.middle import transfer_request_middle
from src.main.api.models.middle.popolnenie_deposit_account_request import PopolnenieDepositAccountRequestMidlle
from src.main.api.specs.response_specs_middle import ResponseSpecs
from src.main.api.models.middle.transfer_request_middle import TransferRequestMiddle

@pytest.mark.api
@pytest.mark.senior

class TestTransfer:
    def test_transfer_middle_valid(self,api_client, user_fixture_senior, db_session: Session):
        response = api_client.admin_steps.login_user(user_fixture_senior)
        api_client.user_steps.authorize(response.token)

        with allure.step('ШАГ 1: Создание счета'):
            account_1 = api_client.user_steps.create_deposit_account(user_fixture_senior)

            deposit_account = PopolnenieDepositAccountRequestMidlle(
                accountId=account_1.id,
                amount=5000
            )
            api_client.user_steps.popolnenie_account(deposit_account)

        with allure.step('ШАГ 1: Создание счета 2'):
            account_2 = api_client.user_steps.create_deposit_account(user_fixture_senior)

            deposit_account2 = PopolnenieDepositAccountRequestMidlle(
                accountId=account_2.id,
                amount=5000
            )
            api_client.user_steps.popolnenie_account(deposit_account2)
            transfer_request_middle = TransferRequestMiddle(
                fromAccountId=account_1.id,
                toAccountId=account_2.id,
                amount=2000
            )

            transfer_response = api_client.user_steps.transfer_credit(transfer_request_middle=transfer_request_middle)

            assert transfer_response.fromAccountIdBalance==3000

            transfer_from_db = TransactionCrud.get_transaction_account(db_session, transfer_request_middle.fromAccountId,transfer_request_middle.toAccountId)
            assert transfer_from_db is not None
            assert transfer_from_db.from_account_id == transfer_response.fromAccountId
            assert transfer_from_db.to_account_id == transfer_response.toAccountId


        # негативный тест на этот же тест-кейс
    def test_transfer_middle_invalid(self, api_client, user_fixture_senior, db_session):
        response = api_client.admin_steps.login_user(user_fixture_senior)
        api_client.user_steps.authorize(response.token)

        with allure.step('Перевод средств'):
            transfer_request_middle = TransferRequestMiddle(
                fromAccountId=56,
                toAccountId=25,
                amount=2000
            )


            api_client.user_steps.execute_negative_request(
                endpoint=Endpoint.TRANSFER_ACCOUNT,
                model=transfer_request_middle,
                expected_spec=ResponseSpecs.request_not_found()
            )
            transfer_from_db_invalid = TransactionCrud.get_transaction_id(db_session, transfer_request_middle.toAccountId)
            assert transfer_from_db_invalid is None
