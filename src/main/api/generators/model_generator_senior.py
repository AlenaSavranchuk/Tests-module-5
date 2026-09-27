import random
import uuid
from typing import Any, get_type_hints, Annotated, get_origin, get_args, Literal
import rstr  # Библиотека для генерации текста по регулярным выражениям
from src.main.api.generators.creation_rule_senior import CreationRuleSenior
import random

class RandomModelGeneratorSenior:

    @staticmethod
    def generate(cls: type) -> Any:
        fields_and_types = get_type_hints(cls, include_extras=True)
        generated_payload = {}

        for field_name, original_type in fields_and_types.items():
            current_rule = None  # Сюда сохраним правило (regex), если оно есть у поля
            clean_type = original_type  # Сюда сохраним чистый тип данных (например, просто str или int)
            if get_origin(clean_type) is Annotated:
                clean_type, *all_annotations = get_args(original_type)
                for annotation in all_annotations:
                    if isinstance(annotation, CreationRuleSenior):
                        current_rule = annotation  # Нашли regex-правило, сохраняем его
            if current_rule:
                final_value = RandomModelGeneratorSenior._create_by_regex(current_rule.regex, clean_type)
            else:
                # ВАЖНО: Мы передаем field_name в скобки, чтобы метод ниже знал, какое поле он сейчас генерирует
                final_value = RandomModelGeneratorSenior._create_by_type(clean_type, field_name)
            generated_payload[field_name] = final_value
        return cls(**generated_payload)

    @staticmethod
    def _create_by_regex(regex_pattern: str, field_type: type) -> Any:
        text_result = rstr.xeger(regex_pattern)  # Создаем случайную строку по шаблону regex
        if field_type is int:
            return int(text_result)
        if field_type is float:
            return float(text_result)

        return text_result

    @staticmethod
    # ВАЖНО: Добавили аргумент field_name со значением по умолчанию "", чтобы не сломать рекурсивные вызовы
    def _create_by_type(field_type: Any, field_name: str = "") -> Any:
        if get_origin(field_type) is Literal:
            return random.choice(get_args(field_type))
        if field_type is str:
            # Умная проверка: если в имени поля есть слово "password", делаем сложный пароль
            if 'password' in field_name.lower():
                return f"Aa1!{str(uuid.uuid4())[:6]}"
            # Для всех остальных текстовых полей (username, email) генерируем чистую латиницу и цифры
            return str(uuid.uuid4())[:8]
        elif field_type is int:
            return random.randint(1, 9999)  # Случайное число
        elif field_type is float:
            return round(random.uniform(0.0, 100.0), 2)  # Случайное дробное число
        elif field_type is bool:
            return random.choice([True, False])  # Случайный True или False
        elif field_type is list:
            return [str(uuid.uuid4())[:5]]  # Список с одной случайной короткой строкой
        elif isinstance(field_type, type):
            # Если тип поля — это ДРУГАЯ модель (вложенный класс), запускаем генератор рекурсивно для неё
            return RandomModelGeneratorSenior.generate(field_type)

        return None  # Если тип неизвестен, возвращаем пустоту
