import logging
from typing import Any, List
import pytest
from src.main.api.clasess.api_manager import ApiManager
from src.main.api.models.mentor.create_user_response import CreateUserResponse
import logging


@pytest.fixture
def created_obj():
    objects: List[Any] = []
    yield objects
    clean_users(objects)


# Функция-помощник, которая берет список созданных объектов и удаляет их из системы.
# ':List[Any]' указывает, что на вход ожидается список элементов любого типа.
def clean_users(objects: List[Any]):
    # Создаем экземпляр ApiManager (который мы разбирали ранее) и передаем ему наш список.
    # Это нужно, чтобы использовать готовые шаги удаления (admin_steps.delete_user),
    # не дублируя логику отправки HTTP-запросов.
    api_manager = ApiManager(objects)

    # Запускаем цикл, который по очереди перебирает каждый объект 'u' из списка 'objects'.
    for u in objects:

        # isinstance(u, CreateUserResponse) — это проверка типа (валидация).
        # Мы проверяем: "Является ли объект 'u' именно ответом о создании пользователя?"
        # Это защищает код от падения, если в список случайно попадет объект другого класса.
        if isinstance(u, CreateUserResponse):

            # Если это пользователь, вызываем админский шаг удаления, вытаскивая ID из объекта: u.id
            api_manager.admin_steps.delete_user(u.id)
        else:

            # Если объект оказался другого типа (не CreateUserResponse), мы не можем прочитать '.id'
            # обычным путем, поэтому пишем предупреждение в логи, чтобы не ломать весь процесс очистки.
            logging.warning(f'Error in delete user_id: {u.id}')
