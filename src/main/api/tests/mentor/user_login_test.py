import pytest
from src.main.api.models.mentor.login_user_request import LoginUserRequest
from src.main.api.models.mentor.create_user_request import CreateUserRequest
from src.main.api.requests.login_user_requester import LoginUserRequester
from src.main.api.specs.request_specs_mentor import RequestSpecs
from src.main.api.specs.response_specs_mentor import ResponseSpecs
from src.main.api.requests.create_user_requester import CreateUserRequester

# тест junior
# @pytest.mark.api
# class TestUserLogin():
#     def test_login_admin(self):
#         login_admin_response = requests.post(
#             url='http://localhost:4111/api/auth/token/login',
#             json={
#                 "username": "admin",
#                 "password": "123456"
#             },
#             headers={
#                 "Content-Type": "application/json",
#                 "accept": "application/json"
#             }
#         )
#
#         assert login_admin_response.status_code == 200
#         assert login_admin_response.json()['user']['username'] == 'admin'
#         assert login_admin_response.json()['user']['role'] == 'ROLE_ADMIN'
#
#
#     def test_login_user(self):
#         login_admin_response = requests.post(
#             url='http://localhost:4111/api/auth/token/login',
#             json={
#                 "username": "admin",
#                 "password": "123456"
#             },
#             headers={
#                 "Content-Type": "application/json",
#                 "accept": "application/json"
#             }
#         )
#
#         assert login_admin_response.status_code == 200
#         token = login_admin_response.json()['token']
#
#
#         create_user_response = requests.post(
#                 url = "http://localhost:4111/api/admin/create",
#                 json = {
#                     "username": "Max45",
#                     "password": "Pas!sw0rd",
#                     "role": "ROLE_USER"
#                 },
#                 headers = {
#                     'Content-Type': "application/json",
#                     'Authorization': f"Bearer {token}"
#                 }
#             )
#
#         login_user_response = requests.post(
#             url = "http://localhost:4111/api/auth/token/login",
#             json = {
#                 "username": "Max45",
#                 "password": "Pas!sw0rd",
#             },
#             headers={
#                 'Content-Type': "application/json",
#                 'accept' : "application/json"
#             }
#         )
#
#         assert login_user_response.status_code == 200
#         assert login_user_response.json()['user']['username'] == 'Max45'
#         assert login_user_response.json()['user']['role'] == 'ROLE_USER'


# @pytest.mark.api
# # тест middle
# class TestUserLogin:
#     def test_login_admin(self):
#         login_user_request = LoginUserRequest(username="admin", password="123456")
#
#         response = LoginUserRequester(
#             request_spec = RequestSpecs.unauth_headers(),
#             response_spec= ResponseSpecs.request_ok()
#         ).post(login_user_request)
#
#
#         assert login_user_request.username == response.user.username
#         assert response.user.role == "ROLE_ADMIN"
#
#
#     def test_login_user(self):
#         create_user_request = CreateUserRequest(username="Max787888", password="Pas!sw0rd", role="ROLE_USER")
#         # создаем пользователя
#         CreateUserRequester(
#             request_spec=RequestSpecs.auth_admin_headers(username='admin', password='123456'),
#             response_spec=ResponseSpecs.request_ok()
#         ).post(create_user_request)
#
#         # логинимся пользователем
#         login_user_request = LoginUserRequest(username='Max787888', password='Pas!sw0rd')
#
#         response = LoginUserRequester(
#             request_spec=RequestSpecs.unauth_headers(),
#             response_spec=ResponseSpecs.request_ok()
#         ).post(login_user_request)
#
#         assert response.user.username == response.user.username
#         assert response.user.role == "ROLE_USER"


@pytest.mark.api
# тест senior
class TestUserLogin:
    def test_login_admin(self, api_manager):
        login_user_request = LoginUserRequest(username="admin", password="123456")
        response = api_manager.admin_steps.login_user(login_user_request)

        assert login_user_request.username == response.user.username
        assert response.user.role == "ROLE_ADMIN"


    def test_login_user(self, api_manager,create_user_request):
        response = api_manager.admin_steps.login_user(create_user_request)


        assert create_user_request.username == response.user.username
        assert response.user.role == "ROLE_USER"
