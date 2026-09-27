import pytest
from src.main.api.db.engine import SessionLocal, engine
from src.main.api.db.models.user_table import User
from src.main.api.db.models.account_table import Account

@pytest.fixture(scope='function')
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionLocal(bind=connection)
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()
