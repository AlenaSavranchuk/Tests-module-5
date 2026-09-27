import pytest
from src.main.api.clasess.api_manager_senior import ApiManagerSenior

@pytest.fixture
def api_client(create_obj):
    # Это "пульт управления", который выдает тесту готовые инструменты для работы.
    # Мы передаем сюда общую "корзину для мусора" (created_obj), чтобы все шаги складывали созданные объекты в одно место.
    return ApiManagerSenior(create_obj)

