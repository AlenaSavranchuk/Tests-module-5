import pytest
import allure
from sqlalchemy.orm import Session
from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.fixtures.db_fixture import db_session
from src.main.api.specs.request_specs_middle import RequestSpecs
from src.main.api.specs.response_specs_middle import ResponseSpecs
from src.main.api.models.middle.transfer_request_middle import TransferRequestMiddle
from src.main.api.requests.requesters_middle.transfer_requester_middle import TransferRequesterMiddle
from src.main.api.generators.data_generator import DataGenerator

@pytest.mark.api
@pytest.mark.middle

class TestTransfer:
    # позитивный тест
    def test_transfer_middle_valid(self,standart_role_plus_accounts_popolnenie: dict, db_session: Session):
        account_id1 = standart_role_plus_accounts_popolnenie['account_1']
        account_id2 = standart_role_plus_accounts_popolnenie['account_2']
        amount = standart_role_plus_accounts_popolnenie['deposit_amount']
        user_spec = standart_role_plus_accounts_popolnenie['user_spec']
        balance_1_before = AccountCrudDb.get_account_balance(db_session, account_id1)
        balance_2_before = AccountCrudDb.get_account_balance(db_session, account_id2)

        with allure.step('Переводим со счета 1 на счет 2'):
            transfer_accounts = TransferRequestMiddle(
                fromAccountId=account_id1,
                toAccountId=account_id2,
                amount=amount
            )

            transfer_accounts_response = TransferRequesterMiddle(
                request_speck_middle=user_spec,
                response_speck_middle=ResponseSpecs.request_ok(),
            ).post(transfer_accounts)

            allure.attach(
                body=transfer_accounts_response.model_dump_json(),  # Что прикрепляем (текст ответа)
                name="Ответ сервера (ожидается статус-код 200)",  # Как это будет называться в отчете
                attachment_type=allure.attachment_type.JSON  # Говорим Allure красиво подсветить JSON
            )

        db_session.expire_all()

        assert transfer_accounts_response.fromAccountId == transfer_accounts.fromAccountId
        assert transfer_accounts_response.toAccountId == transfer_accounts.toAccountId

        balance_1_after = AccountCrudDb.get_account_balance(db_session, account_id1)
        balance_2_after = AccountCrudDb.get_account_balance(db_session, account_id2)
        assert transfer_accounts_response.fromAccountIdBalance == balance_1_after
        assert balance_1_before - amount == balance_1_after
        assert balance_2_before + amount == balance_2_after


        # негативный тест на этот же тест-кейс (нет токена авторизации)
    def test_transfer_middle_invalid(self, user_with_accounts: dict, db_session: Session):
        with allure.step('1. Пополнение счета'):
            account_id1 = user_with_accounts["account_1"]
            account_id2 = user_with_accounts["account_2"]
            test_data = DataGenerator.get_credit_data()
            user_spec = RequestSpecs.unauth_headers()
            balance_1_before = AccountCrudDb.get_account_balance(db_session, account_id1)

            with allure.step('1. Переводим со счета 1 на счет 2'):
                transfer_accounts = TransferRequestMiddle(
                    fromAccountId=account_id1,
                    toAccountId=account_id2,
                    amount=test_data['deposit_amount']
                )

            transfer_accounts_response = TransferRequesterMiddle(
                request_speck_middle=user_spec,
                response_speck_middle=ResponseSpecs.request_unauthorized(),
            ).post(transfer_accounts)

            allure.attach(
                body=transfer_accounts_response.text,  # Что прикрепляем (текст ответа)
                name="Ответ сервера (ожидается статус-код 401)",  # Как это будет называться в отчете
                attachment_type=allure.attachment_type.JSON
            )# Говорим Allure красиво подсветить JSON

        db_session.expire_all()

        assert 'JWT Token not found' in transfer_accounts_response.text
        balance_1_after = AccountCrudDb.get_account_balance(db_session, account_id1)
        assert balance_1_before == balance_1_after, "Баг! Деньги списались со счета при неавторизованном запросе"