import pytest
import allure
from sqlalchemy.orm import Session

from src.main.api.db.crud.credit_crud import CreditCrudDb
from src.main.api.fixtures.api_fixture_senior import api_client
from src.main.api.fixtures.db_fixture import db_session
from src.main.api.foundation.endpoint_senior import Endpoint
from src.main.api.models.middle import credit_response_middle
from src.main.api.specs.request_specs_middle import RequestSpecs
from src.main.api.models.middle.credit_request_middle import CreditRequestMiddle
from src.main.api.requests.requesters_middle.credit_request_requester_middle import CreditRequestRequesterMiddle
from src.main.api.specs.response_specs_middle import ResponseSpecs

@pytest.mark.api
@pytest.mark.senior

class TestCreditRequest:
    url = "http://localhost:4111"

# позитивный тест на взятие кредита
    def test_credit_request_senior(self, api_client,credit_request_fixture, db_session: Session):
        response = api_client.admin_steps.login_user(credit_request_fixture)
        api_client.user_steps.authorize(response.token)

        with allure.step('ШАГ 1: Взятие кредита'):
            account_1 = api_client.user_steps.create_deposit_account(credit_request_fixture)
            credit_request_senior = CreditRequestMiddle(
                accountId=account_1.id,
                amount=5000,
                termMonths= 11
            )

        credit_response = api_client.user_steps.credit_account(credit_request_middle = credit_request_senior)


        assert credit_request_senior.amount == credit_response.amount
        assert credit_request_senior.termMonths == credit_response.termMonths

        credit_from_db = CreditCrudDb.get_credit_id(db_session,credit_response.creditId)
        assert credit_from_db is not None, f"Кредит с id {credit_response.creditId} не найден в базе данных"
        assert credit_from_db.id == credit_response.creditId, 'Поле id кредита отсутствует в бд'


    # негативный тест на запрос получения кредита на тот же счет, что я уже взяла для первого кредита
    def test_credit_request_senior_invalid(self, api_client, credit_request_fixture, db_session: Session):
        response = api_client.admin_steps.login_user(credit_request_fixture)
        api_client.user_steps.authorize(response.token)

        with allure.step('ШАГ 1: Взятие кредита'):
            account_1 = api_client.user_steps.create_deposit_account(credit_request_fixture)
            credit_request_senior = CreditRequestMiddle(
                accountId=account_1.id,
                amount=5000,
                termMonths=11
            )

            credit_response = api_client.user_steps.credit_account(credit_request_middle=credit_request_senior)

            credit_from_db = CreditCrudDb.get_credit_id(db_session, credit_response.creditId)

            assert credit_from_db.id == credit_response.creditId
            assert credit_request_senior.termMonths == credit_response.termMonths

        with allure.step('ШАГ 2: Попытка взять кредит на тот же счет'):
            credit_request_senior = CreditRequestMiddle(
                accountId=account_1.id,
                amount=5000,
                termMonths=11
            )

            api_client.user_steps.execute_negative_request(
                endpoint=Endpoint.CREDIT_REQUEST,
                model=credit_request_senior,
                expected_spec=ResponseSpecs.request_not_found()
            )

        credit_negative_request= CreditCrudDb.get_credit_id(db_session, credit_from_db.id)
        assert credit_negative_request is not None



