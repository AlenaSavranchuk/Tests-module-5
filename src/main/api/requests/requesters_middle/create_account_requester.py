import requests
from src.main.api.models.middle.create_account_response_middle import CreateAccountResponseMiddle
from src.main.api.requests.requesters_middle.requester_middle import RequesterMiddle


class CreateAccountRequesterMiddle(RequesterMiddle):
    """
    Реквестер для отправки API-запросов на создание банковского счета.
    Наследует базовый URL и авторизационные заголовки (headers) от родительского класса RequesterMiddle.
    """

    def post(self, model=None):
        """
        Отправляет POST-запрос на создание нового счета.

        :param model: Данные для создания счета (на текущий момент не используются в теле запроса).
        :return: Наполненную DTO-модель CreateAccountResponseMiddle с данными созданного счета.
        """
        # 1. Формируем полный URL эндпоинта, подставляя базовый адрес из родительского класса
        url = f'{self.base_url}/api/account/create'

        # 2. Выполняем HTTP POST-запрос, передавая сформированный URL и заголовки авторизации
        response = requests.post(
            url=url,
            headers=self.headers,
        )

        # 3. Валидируем полученный ответ (проверяем HTTP-статус код и общую структуру)
        self.response_speck_middle(response)

        # 4. Превращаем JSON-ответ в словарь, распаковываем его через (**) и возвращаем в виде типизированной DTO-модели
        return CreateAccountResponseMiddle(**response.json())
