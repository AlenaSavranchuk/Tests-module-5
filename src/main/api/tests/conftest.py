# import pytest
# import requests
# import uuid
#
# # обычная фикстура
# @pytest.fixture
# def user_with_accounts():
#     url = "http://localhost:4111"
#     username = f"Max{uuid.uuid4().hex[:6]}"
#     password = "Pas!sw0rd"
#     # залогиниваем админа
#     login_admin_response = requests.post(
#         url=f'{url}/api/auth/token/login',
#         json={
#             "username": "admin",
#             "password": "123456"
#         },
#         headers={
#             "Content-Type": "application/json",
#             "accept": "application/json"
#         }
#     )
#     # проверяем, правильно ли мы залогинили админа
#     assert login_admin_response.status_code == 200
#     token = login_admin_response.json()['token']
#
#     # создаем юзера
#     create_user_response = requests.post(
#         url=f"{url}/api/admin/create",
#         json={
#             "username": username,
#             "password": password,
#             "role": "ROLE_USER"
#         },
#         headers={
#             'Content-Type': "application/json",
#             'Authorization': f"Bearer {token}"
#         }
#     )
#
#     # проверяем, правильно ли мы создали юзера и верные ли у него роль\имя
#     assert create_user_response.status_code == 200
#     assert create_user_response.json().get('username') == username
#     assert create_user_response.json().get('role') == 'ROLE_USER'
#
#     login_user_response = requests.post(
#         url=f'{url}/api/auth/token/login',
#         json={
#             "username": username,
#             "password": password,
#         },
#         headers={
#             "Content-Type": "application/json",
#             "accept": "application/json"
#         }
#     )
#     # проверяем логин юзера и сохраняем его токен на авторизацию
#     assert login_user_response.status_code == 200
#     token_user = login_user_response.json()['token']
#
#     # создаем банковский счет 1
#     create_deposit_account_response_valid1 = requests.post(
#         url=f'{url}/api/account/create',
#         json={},
#         headers={
#             'accept': 'application/json',
#             'Authorization': f"Bearer {token_user}"
#         }
#     )
#
#     # проверяем, создался ли счет и сохраняем айди счета
#     assert create_deposit_account_response_valid1.status_code == 201
#     account_id1 = create_deposit_account_response_valid1.json()['id']
#
#     # создаем банковский счет 2
#     create_deposit_account_response_valid2 = requests.post(
#         url=f'{url}/api/account/create',
#         json={},
#         headers={
#             'accept': 'application/json',
#             'Authorization': f"Bearer {token_user}"
#         }
#     )
#
#     # проверяем, создался ли счет и сохраняем айди счета
#     assert create_deposit_account_response_valid2.status_code == 201
#     account_id2 = create_deposit_account_response_valid2.json()['id']
#
# # собираем итог работы всех шагов в один словарь
#     return {
#         "token_user": token_user,
#         "account_1": account_id1,
#         "account_2": account_id2
#     }
#
#
# # фикстура, где роль юзера специальная для выдачи кредита
# @pytest.fixture
# def secret_credit_user_with_accounts():
#     url = "http://localhost:4111"
#     username = f"Max{uuid.uuid4().hex[:6]}"
#     password = "Pas!sw0rd"
#     # залогиниваем админа
#     login_admin_response = requests.post(
#         url=f'{url}/api/auth/token/login',
#         json={
#             "username": "admin",
#             "password": "123456"
#         },
#         headers={
#             "Content-Type": "application/json",
#             "accept": "application/json"
#         }
#     )
#     # проверяем, правильно ли мы залогинили админа
#     assert login_admin_response.status_code == 200
#     token = login_admin_response.json()['token']
#
#     # создаем юзера
#     create_user_response = requests.post(
#         url=f"{url}/api/admin/create",
#         json={
#             "username": username,
#             "password": password,
#             "role": "ROLE_CREDIT_SECRET"
#         },
#         headers={
#             'Content-Type': "application/json",
#             'Authorization': f"Bearer {token}"
#         }
#     )
#
#     # проверяем, правильно ли мы создали юзера и верные ли у него роль\имя
#     assert create_user_response.status_code == 200
#     assert create_user_response.json().get('username') == username
#     assert create_user_response.json().get('role') == 'ROLE_CREDIT_SECRET'
#
#     login_user_response = requests.post(
#         url=f'{url}/api/auth/token/login',
#         json={
#             "username": username,
#             "password": password,
#         },
#         headers={
#             "Content-Type": "application/json",
#             "accept": "application/json"
#         }
#     )
#     # проверяем логин юзера и сохраняем его токен на авторизацию
#     assert login_user_response.status_code == 200
#     token_user = login_user_response.json()['token']
#
#     # создаем банковский счет 1
#     create_deposit_account_response_valid1 = requests.post(
#         url=f'{url}/api/account/create',
#         json={},
#         headers={
#             'accept': 'application/json',
#             'Authorization': f"Bearer {token_user}"
#         }
#     )
#
#     # проверяем, создался ли счет и сохраняем айди счета
#     assert create_deposit_account_response_valid1.status_code == 201
#     account_id1 = create_deposit_account_response_valid1.json()['id']
#
#     # создаем банковский счет 2
#     create_deposit_account_response_valid2 = requests.post(
#         url=f'{url}/api/account/create',
#         json={},
#         headers={
#             'accept': 'application/json',
#             'Authorization': f"Bearer {token_user}"
#         }
#     )
#
#     # проверяем, создался ли счет и сохраняем айди счета
#     assert create_deposit_account_response_valid2.status_code == 201
#     account_id2 = create_deposit_account_response_valid2.json()['id']
#
#     # собираем итог работы всех шагов в один словарь
#     return {
#         "token_user": token_user,
#         "account_1": account_id1,
#         "account_2": account_id2
#     }


pytest_plugins = [
    "src.main.api.fixtures.api_fixture_senior",
    "src.main.api.fixtures.user_fixture_senior",
    "src.main.api.fixtures.credit_request_fixture",
    "src.main.api.fixtures.object_fixture_senior",
    "src.main.api.fixtures.db_fixture",
    "src.main.api.fixtures.api_fixture",
    "src.main.api.fixtures.object_fixture",


]

