import pytest
import allure
from sqlalchemy.orm import Session
from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.specs.request_specs_middle import RequestSpecs
from src.main.api.models.middle.popolnenie_deposit_account_request import PopolnenieDepositAccountRequestMidlle
from src.main.api.requests.requesters_middle.popolnenie_deposit_requester_middle import PopolnenieDepositRequesterMiddle
from src.main.api.specs.response_specs_middle import ResponseSpecs
from src.main.api.generators.data_generator import DataGenerator

@pytest.mark.api
@pytest.mark.middle

class TestDepositAccount:
    def test_bank_account_deposit_valid(self,user_with_accounts: dict, db_session: Session):
        account_id1 = user_with_accounts['account_1']
        test_data = DataGenerator.get_credit_data()
        user_spec = user_with_accounts['user_spec']
        balance_before = AccountCrudDb.get_account_balance(db_session, account_id1)

        with allure.step('Пополняем счет'):
            popolnenie_deposit_account =PopolnenieDepositAccountRequestMidlle(
                accountId = account_id1,
                amount = test_data['deposit_amount'],
            )

            popolnenie_deposit_account = PopolnenieDepositRequesterMiddle(
                request_speck_middle=user_spec,
                response_speck_middle=ResponseSpecs.request_ok(),
            ).post(popolnenie_deposit_account)

            allure.attach(
                body=popolnenie_deposit_account.model_dump_json(),  # Что прикрепляем (текст ответа)
                name="Ответ сервера (ожидается статус-код 200)",  # Как это будет называться в отчете
                attachment_type=allure.attachment_type.JSON  # Говорим Allure красиво подсветить JSON
            )

        assert popolnenie_deposit_account.balance == test_data['deposit_amount'], f'Оишибка: баланс в запросе на пополнение не равен балансу в запросе ответа от сервера'

        popolnenie_deposit_account_db = AccountCrudDb.get_account_balance(db_session, account_id1)
        assert popolnenie_deposit_account_db == balance_before + test_data['deposit_amount'], f'Ошибка: баланс рассчитан неверно'

    # негативный тест на пополнение счета, где не передается токен авторизации
    def test_bank_account_deposit_invalid(self,user_with_accounts: dict, db_session: Session):
        account_id1 = user_with_accounts['account_1']
        test_data = DataGenerator.get_credit_data()
        balance_before = AccountCrudDb.get_account_balance(db_session, account_id1)

        # настраиваем спецификацию запроса без токена авторизации, только заголовки базовые
        user_spec = RequestSpecs.unauth_headers()

        with allure.step('Пополняем счет'):
            bank_account_deposit_invalid = PopolnenieDepositAccountRequestMidlle(
                accountId = account_id1,
                amount = test_data['deposit_amount'],
            )

            pop = PopolnenieDepositRequesterMiddle(
                request_speck_middle=user_spec,
                response_speck_middle=ResponseSpecs.request_unauthorized(),
            ).post(bank_account_deposit_invalid)

            allure.attach(
                body=pop.text,  # Что прикрепляем (текст ответа)
                name="Ответ сервера (ожидается статус-код 401)",  # Как это будет называться в отчете
                attachment_type=allure.attachment_type.JSON  # Говорим Allure красиво подсветить JSON
            )

        db_session.rollback()
        balance_after = AccountCrudDb.get_account_balance(db_session, account_id1)

        assert pop.status_code == 401, f'Ошибка: вернулся не ожидаемый статус-код: {pop.status_code}'
        assert balance_before == balance_after, f'Ошибка: баланс изменился после не авторизованного запроса'
