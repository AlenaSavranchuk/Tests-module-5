import requests
from src.main.api.models.middle.popolnenie_deposit_account_response import PopolnenieDepositAccountResponseMiddle
from src.main.api.requests.requesters_middle.requester_middle import RequesterMiddle


class PopolnenieDepositRequesterMiddle(RequesterMiddle):
    def post (self, popolnenie_deposit_account_request):
        url = f'{self.base_url}/account/deposit'.replace('/api/api', '/api')
        response = requests.post(
            url=url,
            json=popolnenie_deposit_account_request.model_dump(),
            headers=self.headers
        )

        self.response_speck_middle(response)

        if response.status_code in (200, 201):
            return PopolnenieDepositAccountResponseMiddle(**response.json())
        else:
            return response  # Для 401, 400 и других ошибок возвращаем сырой ответ
