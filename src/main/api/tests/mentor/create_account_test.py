import pytest
from sqlalchemy.orm import Session
from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.models.mentor.create_user_request import CreateUserRequest
from src.main.api.clasess.api_manager import ApiManager


@pytest.mark.api
# тест senior
class TestCreateAccount:
    def test_account_creation(self, db_session: Session, user_fixture_senior: CreateUserRequest, api_manager: ApiManager):
        response = api_manager.user_steps.create_account(user_fixture_senior)

        assert response.balance == 0

        account_from_db = AccountCrudDb.get_account_by_id(db_session, response.id)
        assert account_from_db.id == response.id, 'Аккаунт не создан, id аккаунта нет в бд'
        assert account_from_db.balance is not None, 'Поле баланса для созданного аккаунта отсуствует в бд'