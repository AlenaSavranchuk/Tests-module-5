# Этот класс описывает правило генерации текстовых данных с помощью регулярных выражений.
# Он используется генератором моделей (например, `RandomModelGenerator`), чтобы знать,
# по какому именно шаблону (regex) автоматически создавать случайные строки (email, имена, телефоны).

from dataclasses import dataclass

@dataclass
class CreationRuleSenior:
    regex: str