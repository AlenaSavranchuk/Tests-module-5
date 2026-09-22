import pytest
from sqlalchemy.orm import Session
from src.main.api.clasess.api_manager import ApiManager
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.mentor.create_user_request import CreateUserRequest
from src.main.api.db.crud.user_crud import UserCrudDb


# тест senior
@pytest.mark.api
class TestCreateUser:
    @pytest.mark.parametrize(
        'create_user_request',
        [RandomModelGenerator.generate(CreateUserRequest)]
    )
    def test_create_user_valid(self, api_manager: ApiManager, create_user_request: CreateUserRequest, db_session: Session):
        response = api_manager.admin_steps.create_user(create_user_request)

        assert create_user_request.username == response.username
        assert create_user_request.role == response.role

        user_from_db= UserCrudDb.get_user_by_username(db_session, create_user_request.username)
        assert user_from_db.username == create_user_request.username, 'Созданного пользователя нет в бд '



    @pytest.mark.parametrize(
        "username, password",
        [
            ('фбв', 'Pas!sw0rd'),
            ('ab', 'Pas!sw0rd'),
            ('abv!', 'Pas!sw0rd'),
            ('Maxx1', 'Pas!sw0rд'),
            ('Maxx2', 'Pas!sw0'),
            ('Maxx3', 'pas!sw0rd'),
            ('Maxx4', 'PASS!SWORD'),
            ('Maxx5', 'PASSWORD'),
            ('abv!', 'PAS!SWRRD'),
        ]
    )

    def test_create_user_invalid(self, username, password, api_manager, db_session: Session):

        create_user_request = CreateUserRequest(username=username, password=password, role="ROLE_USER")
        api_manager.admin_steps.create_invalid(create_user_request)

        user_from_db= UserCrudDb.get_user_by_username(db_session, username)
        assert user_from_db is None, 'Пользователь создан,ошибка'
