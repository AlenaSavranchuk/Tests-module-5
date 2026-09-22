from unittest import addModuleCleanup

import pytest
import allure
from sqlalchemy.orm import Session

from src.main.api.db.crud.transaction_crud import TransactionCrud
from src.main.api.fixtures.api_fixture_senior import api_client
from src.main.api.fixtures.db_fixture import db_session
from src.main.api.foundation.endpoint_senior import Endpoint
from src.main.api.specs.request_specs_middle import RequestSpecs
from src.main.api.models.middle.popolnenie_deposit_account_request import PopolnenieDepositAccountRequestMidlle
from src.main.api.requests.requesters_middle.popolnenie_deposit_requester_middle import PopolnenieDepositRequesterMiddle
from src.main.api.specs.response_specs_middle import ResponseSpecs

@pytest.mark.api
@pytest.mark.senior
class TestDepositAccount:
    def test_bank_account_deposit_valid(self, api_client, credit_request_fixture, db_session: Session):
        response = api_client.admin_steps.login_user(credit_request_fixture)
        api_client.user_steps.authorize(response.token)

        with allure.step('ШАГ 1: Создание счета'):
            account_1 = api_client.user_steps.create_deposit_account(credit_request_fixture)

            deposit_account = PopolnenieDepositAccountRequestMidlle(
                accountId=account_1.id,
                amount=5000
            )

        with allure.step('ШАГ 2: Пополнение счета'):
            deposit_response = api_client.user_steps.popolnenie_account(popolnenie_deposit_account_request=deposit_account)

            assert deposit_response.balance == 5000
            assert deposit_response.id == account_1.id

            # проверяем сумму пополнения
            deposit_from_db = TransactionCrud.get_transaction_id(db_session, deposit_account.accountId)
            assert deposit_from_db is not None
            assert deposit_from_db.amount == deposit_account.amount

    # негативный тест на пополнение счета, где у нас нет токена авторизации
    def test_bank_account_deposit_invalid(self,api_client, credit_request_fixture, db_session: Session):
        api_client.admin_steps.login_user(credit_request_fixture)

        with allure.step('Пополнение счета'):
            deposit_account = PopolnenieDepositAccountRequestMidlle(
                accountId=25,
                amount=5000
            )

            api_client.user_steps.execute_negative_request(
                endpoint=Endpoint.POPOLNENIE_ACCOUNT,
                model=deposit_account,
                expected_spec=ResponseSpecs.request_unauthorized()
            )

            deposit_from_db = TransactionCrud.get_transaction_id(db_session,deposit_account.accountId)
            assert deposit_from_db is None

