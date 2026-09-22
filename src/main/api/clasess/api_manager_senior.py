from typing import List, Any
from src.main.api.steps.admin_steps_senior import AdminSteps
from src.main.api.steps.user_steps_senior import UserSteps

class ApiManagerSenior:
    # Инициализируем менеджер и передаем единый список для отслеживания созданных объектов
    def __init__(self, created_obj: List[Any]):
        admin_steps: AdminSteps
        user_steps: UserSteps

        # Шаги админа: делят общий список created_obj для фиксации созданных юзеров
        self.admin_steps = AdminSteps(created_obj)
        # Шаги пользователя: используют тот же список (например, для созданных постов/комментов)
        self.user_steps = UserSteps(created_obj)
