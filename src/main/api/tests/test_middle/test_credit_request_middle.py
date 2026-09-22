import requests
import pytest
import allure
from src.main.api.specs.request_specs_middle import RequestSpecs
from src.main.api.models.middle.credit_request_middle import CreditRequestMiddle
from src.main.api.requests.requesters_middle.credit_request_requester_middle import CreditRequestRequesterMiddle
from src.main.api.specs.response_specs_middle import ResponseSpecs
@pytest.mark.api
@pytest.mark.middle

class TestCreditRequest:
    url = "http://localhost:4111"
# функция на кредитик с фикстурой,у которой секретная роль для юзера 
    def test_credit_request_valid(self,secret_credit_user_with_accounts):
        #  Подготовка данных из фикстуры (токен роли секретной и ID аккаунта)
        token_user = secret_credit_user_with_accounts ['token_user']
        account_2 = secret_credit_user_with_accounts['account_2']

        # Настраиваем спецификацию запроса: генерируем базовые заголовки и добавляем токен авторизации
        user_spec = RequestSpecs.unauth_headers()
        user_spec['headers']['Authorization'] = f"Bearer {token_user}"

        with allure.step('1. Запрос на кредит'):
            credit_request = CreditRequestMiddle(
                accountId = account_2,
                amount = 5000,
                termMonths = 3
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

    # негативный тест на запрос получения кредита на тот же счет, что я уже взяла для первого кредита
    def test_credit_request_invalid(self,secret_credit_user_with_accounts):
        token_user = secret_credit_user_with_accounts['token_user']
        account_2 = secret_credit_user_with_accounts['account_2']

        # Настраиваем спецификацию запроса: генерируем базовые заголовки и добавляем токен авторизации
        user_spec = RequestSpecs.unauth_headers()
        user_spec['headers']['Authorization'] = f"Bearer {token_user}"

        with allure.step('1. Запрос на кредит'):
            credit_request = CreditRequestMiddle(
                accountId=account_2,
                amount=5000,
                termMonths=3
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
                amount=5000,
                termMonths=3
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


