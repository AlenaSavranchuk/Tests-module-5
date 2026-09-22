from typing import Any, get_origin, Annotated, get_args
from typing import get_type_hints
import rstr
from src.main.api.generators.creation_rule import CreationRule
import uuid
import random

class RandomModelGenerator:
    @staticmethod
    def generate(cls: type) -> Any:
        # Достаем все поля и типы данных из класса (включая метаданные `Annotated`), формируя словарь.
        type_hints = get_type_hints(cls, include_extras=True)
        # Пустой словарь, куда мы поочередно сложим сгенерированные пары {"имя_поля": значение}.
        init_data = {}
        for field_name, annotated_type in type_hints.items():
            rule = None  # Переменная для хранения правила генерации (regex), изначально пустая.
            actual_type = annotated_type  # Переменная для чистого типа данных (int, str), очищенного от оберток.

            if get_origin(actual_type) is Annotated: # Разделяем обертку: получаем чистый тип данных (`actual_type`) и список всех метаданных (`annotations`).
                actual_type, *annotations = get_args(annotated_type)
                for ann in annotations:
                    if isinstance(ann, CreationRule):
                        rule = ann

            if rule:
                value = RandomModelGenerator._generate_from_regex(rule.regex, actual_type)
            else:
                value = RandomModelGenerator._generate_value(actual_type)
            init_data[field_name] = value
        return cls(**init_data)

    @staticmethod
    def _generate_from_regex(regex: str, field_type: type) -> Any:
        generated = rstr.xeger(regex)
        if field_type is int:
            return int(generated)
        if field_type is float:
            return float(generated)
        return generated

    @staticmethod
    def _generate_value(field_type) -> Any:
        if field_type is str:
            return str(uuid.uuid4())[:8]
        elif field_type is int:
            return random.randint(1, 9999)
        elif field_type is float:
            return round(random.uniform(0, 100.), 2)
        elif field_type is bool:
            return random.choice([True, False])
        elif field_type is list:
            return [str(uuid.uuid4())[:5]]
        elif isinstance(field_type, type):
            return RandomModelGenerator.generate(field_type)
        return None


