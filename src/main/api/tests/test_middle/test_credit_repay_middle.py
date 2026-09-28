from operator import abs
import allure
import pytest
from sqlalchemy.orm import Session
from src.main.api.db.crud.credit_crud import CreditCrudDb
from src.main.api.fixtures.db_fixture import db_session
from src.main.api.models.middle.credit_repay_request_middle import CreditRepayRequestMiddle
from src.main.api.requests.requesters_middle.credit_repay_requester_middle import CreditRepayRequesterMiddle
from src.main.api.specs.response_specs_middle import ResponseSpecs
from src.main.api.generators.data_generator import DataGenerator

@pytest.mark.api
@pytest.mark.middle
class TestCreditRepay:
    # позитивный тест
    def test_credit_repay(self, active_credit_for_repay: dict, db_session: Session):
        # подготовка данных из фикстур
        account_1 = active_credit_for_repay['account_id']
        user_spec = active_credit_for_repay['user_spec']

        credit_data = CreditRepayRequestMiddle(
            creditId=active_credit_for_repay['credit_id'],
            accountId=account_1,
            amount=active_credit_for_repay['credit_amount'],
        )

        with allure.step('Запрос на погашение кредита'):
            response = CreditRepayRequesterMiddle(
                request_speck_middle=user_spec,
                response_speck_middle=ResponseSpecs.request_ok()
            ).post(credit_data)

        allure.attach(
            body=response.model_dump_json(),
            name="Ответ сервера (ожидается статус-код 200)",
            attachment_type=allure.attachment_type.JSON
        )

        assert response.creditId == credit_data.creditId, f'Ошибка: id кредита от запроса и id кредита от ответа сервера не совпадают'
        assert response.amountDeposited == credit_data.amount, f'Ошибка: сумма погашения кредита не равна. Ожидалось {credit_data.amount}, фактически: {response.amountDeposited}'

        credit_repay_db = CreditCrudDb.get_credit_id(db_session, active_credit_for_repay['credit_id'])
        assert credit_repay_db is not None, f"Ошибка: кредит с ID {active_credit_for_repay['credit_id']} не найден в БД"
        assert credit_repay_db.balance == 0, f'Ошибка: кредит не погашен полностью, по факту баланс {credit_repay_db.balance}'

    # негативный тест на погашение кредита (с невалидной суммой)
    def test_credit_request_invalid(self, active_credit_for_repay: dict, db_session: Session):
        # подготовка данных из фикстур
        account_1 = active_credit_for_repay['account_id']
        user_spec = active_credit_for_repay['user_spec']

        with allure.step('Негативное погашение'):
            credit_data_invalid = CreditRepayRequestMiddle(
                creditId=active_credit_for_repay['credit_id'],
                accountId=account_1,
                amount=DataGenerator.get_invalid_amount()
            )

            error_response = CreditRepayRequesterMiddle(
                request_speck_middle=user_spec,
                response_speck_middle=ResponseSpecs.request_bad()
            ).post(credit_data_invalid)

        allure.attach(
            body=error_response.text,
            name="Ответ сервера (ожидается статус-код 400)",
            attachment_type=allure.attachment_type.JSON
        )

        assert "amount" in error_response.text.lower(), f'Ошибка: в ответе сервера нет упоминания поля суммы'

        credit_repay_db = CreditCrudDb.get_credit_id(db_session, active_credit_for_repay['credit_id'])
        assert abs(credit_repay_db.balance) == active_credit_for_repay['credit_amount'], f'Ошибка: после неуспешного запроса баланс кредита в БД изменился'

