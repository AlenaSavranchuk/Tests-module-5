import pytest
import allure
from sqlalchemy.orm import Session
from src.main.api.db.crud.credit_crud import CreditCrudDb
from src.main.api.fixtures.db_fixture import db_session
from src.main.api.models.middle.credit_request_middle import CreditRequestMiddle
from src.main.api.requests.requesters_middle.credit_request_requester_middle import CreditRequestRequesterMiddle
from src.main.api.specs.response_specs_middle import ResponseSpecs
from src.main.api.generators.data_generator import DataGenerator
@pytest.mark.api
@pytest.mark.middle

class TestCreditRequest:
# функция на кредитик с фикстурой,у которой секретная роль для юзера 
    def test_credit_request_valid(self,secret_credit_user_with_accounts: dict, db_session: Session):
        account_2 = secret_credit_user_with_accounts['account_2']
        test_data = DataGenerator.get_credit_data()
        user_spec = secret_credit_user_with_accounts['user_spec']

        with allure.step('Запрос на кредит'):
            credit_request = CreditRequestMiddle(
                accountId = account_2,
                amount = test_data['credit_amount'],
                termMonths = test_data['term_months']
            )

        response_data = CreditRequestRequesterMiddle(
            request_speck_middle = user_spec,
            response_speck_middle=ResponseSpecs.request_created()
        ).post(credit_request)

        allure.attach(
            body=response_data.model_dump_json(),  # Текст ответа
            name="Ответ сервера (ожидается статус-код 201)",  # Как это будет называться в отчете
            attachment_type=allure.attachment_type.JSON  # Говорим Allure красиво подсветить JSON
        )

        assert response_data.creditId is not None, f'Ошибка: в ответе сервера ID кредита пустое {response_data.creditId}'
        assert response_data.creditId > 0, f'Ошибка: ID кредита в ответе от сервера должен быть строго больше 0'

        credit_request_db = CreditCrudDb.get_credit_id(db_session, response_data.creditId)
        assert credit_request_db is not None, f'Ошибка: ID кредита в БД не найдена'

    # негативный тест на запрос получения кредита на тот же счет, что я уже взяла для первого кредита
    def test_credit_request_invalid(self,secret_credit_user_with_accounts: dict, db_session: Session):
        account_2 = secret_credit_user_with_accounts['account_2']
        test_data = DataGenerator.get_credit_data()
        user_spec = secret_credit_user_with_accounts['user_spec']

        with allure.step('Запрос на кредит'):
            credit_request = CreditRequestMiddle(
                accountId=account_2,
                amount=test_data['credit_amount'],
                termMonths=test_data['term_months']
            )

        response_data = CreditRequestRequesterMiddle(
            request_speck_middle=user_spec,
            response_speck_middle=ResponseSpecs.request_created()
        ).post(credit_request)

        allure.attach(
            body=response_data.model_dump_json(),  # Текст ответа
            name="Ответ сервера (ожидается статус-код 201)",  # Как это будет называться в отчете
            attachment_type=allure.attachment_type.JSON  # Говорим Allure красиво подсветить JSON
        )

        with allure.step('2. Запрос на второй кредит'):
            credit_request_new2 = CreditRequestMiddle(
                accountId=account_2,
                amount=test_data['credit_amount'],
                termMonths=test_data['term_months']
            )

        response_data_new2= CreditRequestRequesterMiddle(
            request_speck_middle=user_spec,
            response_speck_middle=ResponseSpecs.request_not_found()
        ).post(credit_request_new2)

        allure.attach(
            body=response_data_new2.text,  # Что прикрепляем (текст ответа)
            name="Ответ сервера (ожидается статус-код 404)",  # Как это будет называться в отчете
            attachment_type=allure.attachment_type.JSON  # Говорим Allure красиво подсветить JSON
        )

        credit_request_db = CreditCrudDb.get_credit_count(db_session,account_2)
        assert credit_request_db == 1, f'Ошибка: одидался 1 оформленный кредит, по факту количество: {credit_request_db}'

