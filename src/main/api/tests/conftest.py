import pytest
import requests
import uuid
from src.main.api.generators.data_generator import DataGenerator
from src.main.api.clasess.api_manager_senior import ApiManagerSenior
from src.main.api.models.middle.popolnenie_deposit_account_request import PopolnenieDepositAccountRequestMidlle
from src.main.api.models.middle.credit_request_middle import CreditRequestMiddle
from src.main.api.specs.request_specs_middle import RequestSpecs

# обычная фикстура c 2 счетами
@pytest.fixture
def user_with_accounts():
    url = "http://localhost:4111"
    username = f"Max{uuid.uuid4().hex[:6]}"
    password = "Pas!sw0rd"
    # залогиниваем админа
    login_admin_response = requests.post(
        url=f'{url}/api/auth/token/login',
        json={
            "username": "admin",
            "password": "123456"
        },
        headers={
            "Content-Type": "application/json",
            "accept": "application/json"
        }
    )
    # проверяем, правильно ли мы залогинили админа
    assert login_admin_response.status_code == 200
    token = login_admin_response.json()['token']

    # создаем юзера
    create_user_response = requests.post(
        url=f"{url}/api/admin/create",
        json={
            "username": username,
            "password": password,
            "role": "ROLE_USER"
        },
        headers={
            'Content-Type': "application/json",
            'Authorization': f"Bearer {token}"
        }
    )

    # проверяем, правильно ли мы создали юзера и верные ли у него роль\имя
    assert create_user_response.status_code == 200
    assert create_user_response.json().get('username') == username
    assert create_user_response.json().get('role') == 'ROLE_USER'

    login_user_response = requests.post(
        url=f'{url}/api/auth/token/login',
        json={
            "username": username,
            "password": password,
        },
        headers={
            "Content-Type": "application/json",
            "accept": "application/json"
        }
    )
    # проверяем логин юзера и сохраняем его токен на авторизацию
    assert login_user_response.status_code == 200
    token_user = login_user_response.json()['token']

    # создаем банковский счет 1
    create_deposit_account_response_valid1 = requests.post(
        url=f'{url}/api/account/create',
        json={},
        headers={
            'accept': 'application/json',
            'Authorization': f"Bearer {token_user}"
        }
    )

    # проверяем, создался ли счет и сохраняем айди счета
    assert create_deposit_account_response_valid1.status_code == 201
    account_id1 = create_deposit_account_response_valid1.json()['id']

    # создаем банковский счет 2
    create_deposit_account_response_valid2 = requests.post(
        url=f'{url}/api/account/create',
        json={},
        headers={
            'accept': 'application/json',
            'Authorization': f"Bearer {token_user}"
        }
    )

    # проверяем, создался ли счет и сохраняем айди счета
    assert create_deposit_account_response_valid2.status_code == 201
    account_id2 = create_deposit_account_response_valid2.json()['id']

    # сборка спецификации
    user_spec = RequestSpecs.unauth_headers()
    user_spec['headers']['Authorization'] = f"Bearer {token_user}"

    # собираем итог работы всех шагов в один словарь
    return {
        "token_user": token_user,
        "account_1": account_id1,
        "account_2": account_id2,
        'user_spec': user_spec
    }

# фикстура, где роль юзера специальная для выдачи кредита. тут я создаю 2 счета и все
@pytest.fixture
def secret_credit_user_with_accounts():
    url = "http://localhost:4111"
    username = f"Max{uuid.uuid4().hex[:6]}"
    password = "Pas!sw0rd"
    # залогиниваем админа
    login_admin_response = requests.post(
        url=f'{url}/api/auth/token/login',
        json={
            "username": "admin",
            "password": "123456"
        },
        headers={
            "Content-Type": "application/json",
            "accept": "application/json"
        }
    )
    # проверяем, правильно ли мы залогинили админа
    assert login_admin_response.status_code == 200
    token = login_admin_response.json()['token']

    # создаем юзера
    create_user_response = requests.post(
        url=f"{url}/api/admin/create",
        json={
            "username": username,
            "password": password,
            "role": "ROLE_CREDIT_SECRET"
        },
        headers={
            'Content-Type': "application/json",
            'Authorization': f"Bearer {token}"
        }
    )

    # проверяем, правильно ли мы создали юзера и верные ли у него роль\имя
    assert create_user_response.status_code == 200
    assert create_user_response.json().get('username') == username
    assert create_user_response.json().get('role') == 'ROLE_CREDIT_SECRET'

    login_user_response = requests.post(
        url=f'{url}/api/auth/token/login',
        json={
            "username": username,
            "password": password,
        },
        headers={
            "Content-Type": "application/json",
            "accept": "application/json"
        }
    )
    # проверяем логин юзера и сохраняем его токен на авторизацию
    assert login_user_response.status_code == 200
    token_user = login_user_response.json()['token']

    # создаем банковский счет 1
    create_deposit_account_response_valid1 = requests.post(
        url=f'{url}/api/account/create',
        json={},
        headers={
            'accept': 'application/json',
            'Authorization': f"Bearer {token_user}"
        }
    )

    # проверяем, создался ли счет и сохраняем айди счета
    assert create_deposit_account_response_valid1.status_code == 201
    account_id1 = create_deposit_account_response_valid1.json()['id']

    # создаем банковский счет 2
    create_deposit_account_response_valid2 = requests.post(
        url=f'{url}/api/account/create',
        json={},
        headers={
            'accept': 'application/json',
            'Authorization': f"Bearer {token_user}"
        }
    )

    # проверяем, создался ли счет и сохраняем айди счета
    assert create_deposit_account_response_valid2.status_code == 201
    account_id2 = create_deposit_account_response_valid2.json()['id']

    # сборка спецификации
    user_spec = RequestSpecs.unauth_headers()
    user_spec['headers']['Authorization'] = f"Bearer {token_user}"

    # собираем итог работы всех шагов в один словарь
    return {
        "token_user": token_user,
        "account_1": account_id1,
        "account_2": account_id2,
        "user_spec": user_spec,
        'url': url
    }

# Фикстура использует готового юзера со счетами, авторизует его, делает депозит и берет кредит
@pytest.fixture
def active_credit_for_repay(api_client: ApiManagerSenior, secret_credit_user_with_accounts: dict):

    token_user = secret_credit_user_with_accounts['token_user']
    account_1_id = secret_credit_user_with_accounts['account_1']

    # Собираем спецификацию прямо здесь, один раз для всех тестов
    user_spec = RequestSpecs.unauth_headers()
    user_spec['headers']['Authorization'] = f"Bearer {token_user}"

    # логиним юзера с секретной ролью
    api_client.user_steps.authorize(token_user, role="ROLE_CREDIT_SECRET")

    # Генерируем суммы один раз
    test_data = DataGenerator.get_credit_data()

    # 2. Пополнение счета (Депозит) через модель и шаги
    deposit_data = PopolnenieDepositAccountRequestMidlle(
        accountId=account_1_id,
        amount=test_data["deposit_amount"],
    )
    api_client.user_steps.popolnenie_account(popolnenie_deposit_account_request=deposit_data)

    # 3. Создание кредита через модель и шаги
    credit_creation_data = CreditRequestMiddle(
        accountId=account_1_id,
        amount=test_data["credit_amount"],
        termMonths=test_data["term_months"]
    )
    response_credit = api_client.user_steps.credit_account(credit_request_middle=credit_creation_data)

    # Возвращаем в тест только то, что нужно для финального шага погашения
    return {
        "token_user": token_user,
        "account_id": account_1_id,
        "credit_id": response_credit.creditId,
        "credit_amount": test_data["credit_amount"],
        "user_spec": user_spec
    }


# фикстура, где роль юзера обычна и создание 2 счетов + пополнение 1 счета
@pytest.fixture
def standart_role_plus_accounts_popolnenie(api_client: ApiManagerSenior, user_with_accounts: dict):
    # вытаскиваем данные из фикстур
    token_user = user_with_accounts['token_user']
    account_1_id = user_with_accounts['account_1']
    account_2_id = user_with_accounts['account_2']

    # логиним юзера
    api_client.user_steps.authorize(token_user, role="ROLE_USER")

    # Генерируем суммы один раз
    test_data = DataGenerator.get_credit_data()

    # 2. Пополнение счета через модель и шаги
    deposit_data = PopolnenieDepositAccountRequestMidlle(
        accountId=account_1_id,
        amount=test_data["deposit_amount"],
    )
    api_client.user_steps.popolnenie_account(popolnenie_deposit_account_request=deposit_data)

    # сборка спецификации
    user_spec = RequestSpecs.unauth_headers()
    user_spec['headers']['Authorization'] = f"Bearer {token_user}"

    # собираем итог работы всех шагов в один словарь
    return {
        "token_user": token_user,
        "account_1": account_1_id,
        "account_2": account_2_id,
        'user_spec': user_spec,
        'deposit_amount': deposit_data.amount
    }



pytest_plugins = [
    "src.main.api.fixtures.api_fixture_senior",
    "src.main.api.fixtures.user_fixture_senior",
    "src.main.api.fixtures.credit_request_fixture",
    "src.main.api.fixtures.object_fixture_senior",
    "src.main.api.fixtures.db_fixture",
    "src.main.api.fixtures.api_fixture",
    "src.main.api.fixtures.object_fixture"
]

