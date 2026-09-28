import pytest
from sqlalchemy.orm import Session
from src.main.api.fixtures.db_fixture import db_session
from src.main.api.models.middle.credit_repay_request_middle import CreditRepayRequestMiddle
from src.main.api.specs.response_specs_middle import ResponseSpecs
from src.main.api.models.middle.credit_request_middle import CreditRequestMiddle
from src.main.api.foundation.endpoint_senior import Endpoint
from src.main.api.fixtures.api_fixture_senior import api_client
from src.main.api.clasess.api_manager_senior import ApiManagerSenior
import allure
from src.main.api.generators.data_generator import DataGenerator
from src.main.api.db.crud.credit_crud import CreditCrudDb
from src.main.api.db.models.account_table import Account

@pytest.mark.api
@pytest.mark.senior
class TestCreditRepay:
    # позитивный тест
    def test_credit_repay(self, active_credit_for_repay: dict, api_client: ApiManagerSenior, db_session: Session) -> None:
        balance_before = db_session.query(Account.balance).filter_by(id=active_credit_for_repay["account_id"]).scalar()
        with allure.step('Погашение кредита'):
            repay_data = CreditRepayRequestMiddle(
                creditId=active_credit_for_repay["credit_id"],
                accountId=active_credit_for_repay["account_id"],
                amount=active_credit_for_repay["credit_amount"],
            )
            response_repay = api_client.user_steps.credit_repay(credit_repay_request_middle=repay_data)

        balance_after = db_session.query(Account.balance).filter_by(id=active_credit_for_repay["account_id"]).scalar()

        assert response_repay.creditId is not None, f'Ошибка: {response_repay.creditId} отсутствует в отете сервера'
        assert response_repay.creditId == active_credit_for_repay["credit_id"], f'Ошибка: ID кредита не совпадает с ожидаемым'
        assert balance_before != balance_after, f'Ошибка: баланс до запроса и баланс после запроса не совпадают'

    # негативный тест, когда невозможно взять 2 кредита на 1 счет
    def test_credit_request_invalid(self, api_client: ApiManagerSenior,db_session: Session, active_credit_for_repay: dict) :
        test_data = DataGenerator.get_credit_data()
        with allure.step('Попытка взять второй кредит на тот же счет '):
            repay_data = CreditRequestMiddle(
                accountId=active_credit_for_repay["account_id"],
                amount=active_credit_for_repay["credit_amount"],
                termMonths=test_data["term_months"],
            )

            response_data_invalid = api_client.user_steps.execute_negative_request(
                endpoint=Endpoint.CREDIT_REQUEST,
                model=repay_data,
                expected_spec=ResponseSpecs.request_not_found()
            )

            credit_count = CreditCrudDb.get_credit_count(db_session,active_credit_for_repay["account_id"])
            assert credit_count == 1, f'Ошибка: сумма кредитов не равна 1'





