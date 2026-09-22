import logging
from typing import List, Any
import pytest
from src.main.api.clasess.api_manager import ApiManager
from src.main.api.models.middle.create_user_response_middle import CreateUserResponseMiddle


@pytest.fixture
def create_obj():
    # Создаем пустую корзину (список), куда тесты будут собирать созданные объекты
    objects: List[Any] = []
    # Отдаем этот список в тест. Всё, что написано ниже yield, запустится строго ПОСЛЕ теста
    yield objects
    # Тест завершился, передаем наполненную корзину функции-уборщику (teardown)
    delete_users(objects)


def delete_users(objects: List[Any]):
    # Создаем локальный менеджер и отдаем ему наш список для доступа к методам удаления
    api_manager = ApiManager(objects)
    # По очереди достаем каждый объект из корзины с мусором
    for u in objects:
        # Проверяем: если этот объект является успешным ответом о создании пользователя
        if isinstance(u, CreateUserResponseMiddle):
            # Передаем его уникальный ID в готовый метод админа для физического удаления из БД
            api_manager.admin_steps.delete_user(u.id)
        # Если в корзине оказался объект неизвестного типа, который мы не умеем удалять
        else:
            # Просто выводим тип объекта и сам объект целиком, чтобы Python никогда не падал из-за отсутствия полей
            logging.warning(f'Unknown object in trash bin: {type(u).__name__} -> {u}')

