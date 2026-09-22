from pathlib import Path
from typing import Any
import pytest

# для уровня middle
# from pathlib import Path
# from typing import Any
#
#
# class Config:
#     _isinstance = None
#     _dictionary = {}
#
#     def __new__(cls):
#         if cls._isinstance is None:
#             cls._isinstance = super(Config, cls).__new__(cls)
#             print(f"ТЕКУЩИЙ ФАЙЛ: {__file__}")
#
#         # была постоянная ошибка, в первый день, когда собрала все тесты с видео, что файл не найден. По этому,решила хард прописать путь к папке
#             config_path = Path(r"C:\SUAI\PythonProject\Tasks from module 5\resources\urls.properties")
#
#             if not config_path.exists():
#                 raise FileNotFoundError(f'Config path not found: {config_path}')
#
#             with open(config_path, 'r') as f:
#                 for line in f:
#                     if '=' in line:
#                         key, value = line.split('=')
#                         # Добавили .strip(), чтобы очистить от невидимого переноса строки \n
#                         cls._dictionary[key.strip()] = value.strip()
#
#         return cls._isinstance
#
#     @staticmethod
#     def fetch(key: str, default_value: Any = None) -> Any:
#         try:
#             Config()  # Пробуем прочитать файл
#         except FileNotFoundError:
#             # Если Windows заблокировала файл и вылетела ошибка — нам всё равно!
#             # Мы вручную проверяем ключ и отдаем дефолтное значение
#             if key == 'backendUrl':
#                 return 'http://localhost:4111/api'
#
#         # Если файл прочитался нормально, отдаем значение из словаря
#         # А если словаре пусто, отдаем дефолтное значение 'http://localhost:4111/api'
#         return Config._dictionary.get(key, default_value or 'http://localhost:4111/api')

# файл с классом-помошником, чтобы 1 раз на весь проект прочитать его и запомнить настройки
class ConfigMiddle:
    BASE_URL = {
        'backendURL' : 'http://localhost:4111/api'
    }

# метод внутри класса, переводится как достать, работает как умный поисковик: говорю ему, какой мне параметр нужен, а он идет и забирает его
    @staticmethod
    def fetch(key):
        return ConfigMiddle.BASE_URL[key]





