import pytest
from src.main.api.models.middle.credit_repay_request_middle import CreditRepayRequestMiddle
from src.main.api.requests.requesters_middle.credit_request_requester_middle import CreditRequestRequesterMiddle
from src.main.api.requests.requesters_middle.credit_repay_requester_middle import CreditRepayRequesterMiddle
from src.main.api.specs.request_specs_middle import RequestSpecs
from src.main.api.specs.response_specs_middle import ResponseSpecs
from src.main.api.models.middle.popolnenie_deposit_account_request import PopolnenieDepositAccountRequestMidlle
from src.main.api.requests.requesters_middle.popolnenie_deposit_requester_middle import PopolnenieDepositRequesterMiddle
from src.main.api.models.middle.credit_request_middle import CreditRequestMiddle

@pytest.mark.api
@pytest.mark.middle
class TestCreditRepay:
    url = "http://localhost:4111"

    # позитивный тест
    def test_credit_repay(self, secret_credit_user_with_accounts):
        #  Подготовка данных из фикстуры (токен и ID аккаунта)
        token_user = secret_credit_user_with_accounts['token_user']
        account_1 = secret_credit_user_with_accounts['account_1']

        # Настраиваем спецификацию запроса: генерируем базовые заголовки и добавляем токен авторизации
        user_spec = RequestSpecs.unauth_headers()
        user_spec['headers']['Authorization'] = f"Bearer {token_user}"

        # --- ШАГ 1: Пополнение счета (Депозит) ---
        # Упаковываем данные для пополнения в специальную модель запроса
        deposit_data = PopolnenieDepositAccountRequestMidlle(
            accountId=account_1,
            amount=9000,
        )
        # Курьер отправляет депозит и строго проверяет через ResponseSpecs, что сервер вернул статус 200 OK
        PopolnenieDepositRequesterMiddle(
            request_speck_middle=user_spec,
            response_speck_middle=ResponseSpecs.request_ok()
        ).post(deposit_data)

        # --- ШАГ 2: Создание кредита ---
        # Собираем легкую модель запроса на кредит (только нужные поля бэкенда)
        credit_creation_data = CreditRequestMiddle(
            accountId=account_1,
            amount=5000,
            termMonths=11
        )
        # Отправляем запрос на создание кредита. Ждем статус 201 Created.
        # Результат сохраняем в переменную, так как бэкенд вернет обновленную модель с creditId внутри
        response_credit = CreditRequestRequesterMiddle(
            request_speck_middle=user_spec,
            response_speck_middle=ResponseSpecs.request_created()
        ).post(credit_creation_data)

        # --- ШАГ 3: Погашение кредита ---
        # Собираем модель погашения. Важно: динамически подставляем creditId, полученный из предыдущего шага!
        credit_data = CreditRepayRequestMiddle(
            creditId=response_credit.creditId,
            accountId=account_1,
            amount=5000
        )
        # Отправляем запрос на погашение кредита. Проверяем через спеку, что вернулся статус 200 OK
        CreditRepayRequesterMiddle(
            request_speck_middle=user_spec,
            response_speck_middle=ResponseSpecs.request_ok()
        ).post(credit_data)

    # негативный тест, когда невозможно взять 2 кредита на 1 счет
    def test_credit_request_invalid(self, secret_credit_user_with_accounts):
        # [ARRANGE] Подготовка данных и авторизационных заголовков
        token_user = secret_credit_user_with_accounts['token_user']
        account_1 = secret_credit_user_with_accounts['account_1']

        user_spec = RequestSpecs.unauth_headers()
        user_spec['headers']['Authorization'] = f"Bearer {token_user}"

        # --- ШАГ 1: Создание кредита ---
        # Готовим данные для создания кредита (баланс аккаунта пока равен 0)
        credit_creation = CreditRequestMiddle(
            accountId=account_1,
            amount=5000,
            termMonths=3
        )
        # Создаем реальный кредит в системе, чтобы получить его валидный ID. Ждем 201 Created.
        response_credit = CreditRequestRequesterMiddle(
            request_speck_middle=user_spec,
            response_speck_middle=ResponseSpecs.request_created()
        ).post(credit_creation)

        # --- ШАГ 2: Попытка негативного погашения ---
        # Собираем модель погашения: передаем ID созданного кредита, но выставляем сумму 10000 (на балансе денег нет!)
        credit_data_invalid = CreditRepayRequestMiddle(
            creditId=response_credit.creditId,
            accountId=account_1,
            amount=10000
        )
        # Курьер отправляет запрос. Мы передаем созданную тобой спецификацию request_validation_error(),
        # которая строго проверяет, что сервер отклонил операцию и вернул ошибку бизнес-логики со статусом 422.
        # Благодаря нашему if-условию в реквестере, тест успешно завершится без падения Pydantic-модели!
        CreditRepayRequesterMiddle(
            request_speck_middle=user_spec,
            response_speck_middle=ResponseSpecs.request_validation_error()
        ).post(credit_data_invalid)


