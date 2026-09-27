import pytest
import allure
from sqlalchemy.orm import Session
from src.main.api.db.crud.credit_crud import CreditCrudDb
from src.main.api.fixtures.api_fixture_senior import api_client
from src.main.api.fixtures.db_fixture import db_session
from src.main.api.foundation.endpoint_senior import Endpoint
from src.main.api.models.middle.credit_request_middle import CreditRequestMiddle
from src.main.api.specs.response_specs_middle import ResponseSpecs
from src.main.api.clasess.api_manager_senior import ApiManagerSenior
from src.main.api.generators.data_generator import DataGenerator

@pytest.mark.api
@pytest.mark.senior

class TestCreditRequest:
# позитивный тест
    def test_credit_request_senior(self, api_client: ApiManagerSenior,secret_credit_user_with_accounts: dict, db_session: Session):
        test_data = DataGenerator.get_credit_data()
        api_client.user_steps.authorize(secret_credit_user_with_accounts["token_user"])
        with allure.step('ШАГ 1: Взятие кредита'):
            credit_request_senior = CreditRequestMiddle(
                accountId=secret_credit_user_with_accounts['account_1'],
                amount=test_data['credit_amount'],
                termMonths= test_data['term_months']
            )
            credit_response = api_client.user_steps.credit_account(credit_request_middle = credit_request_senior)

        assert credit_request_senior.amount == credit_response.amount
        assert credit_request_senior.termMonths == credit_response.termMonths

        credit_from_db = CreditCrudDb.get_credit_id(db_session,credit_response.creditId)
        assert credit_from_db is not None, f"Кредит с id {credit_response.creditId} не найден в базе данных"
        assert credit_from_db.amount == credit_request_senior.amount

    # негативный тест на запрос получения кредита на тот же счет, что я уже взяла для первого кредита
    def test_credit_request_senior_invalid(self, api_client: ApiManagerSenior,secret_credit_user_with_accounts: dict, db_session: Session, active_credit_for_repay: dict):
        test_data = DataGenerator.get_credit_data()
        active_account = active_credit_for_repay['account_id']
        api_client.user_steps.authorize(secret_credit_user_with_accounts["token_user"])

        with allure.step('Попытка взять кредит на тот же счет'):
            credit_request_senior = CreditRequestMiddle(
                accountId=active_account,
                amount=test_data['credit_amount'],
                termMonths=test_data['term_months']
            )

            api_client.user_steps.execute_negative_request(
                endpoint=Endpoint.CREDIT_REQUEST,
                model=credit_request_senior,
                expected_spec=ResponseSpecs.request_not_found()
            )

        credit_negative_request_db=CreditCrudDb.get_credit_count(db_session,active_credit_for_repay["account_id"])
        assert credit_negative_request_db == 1



