import pytest
from src.main.api.generators.model_generator_senior import RandomModelGeneratorSenior
from src.main.api.models.middle.create_user_request_middle import CreateUserRequestMiddle

@pytest.fixture
def credit_request_fixture(api_client):
    user_request = RandomModelGeneratorSenior.generate(CreateUserRequestMiddle)
    user_request.role = 'ROLE_CREDIT_SECRET'
    api_client.admin_steps.create_user(user_request)
    return user_request