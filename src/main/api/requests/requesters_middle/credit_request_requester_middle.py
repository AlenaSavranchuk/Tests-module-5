import requests
from src.main.api.requests.requesters_middle.requester_middle import RequesterMiddle
from src.main.api.models.middle.credit_response_middle import CreditResponseMiddle

class CreditRequestRequesterMiddle(RequesterMiddle):
        def post(self, credit_repay_request_middle):
            url = f'{self.base_url}/credit/request'.replace('/api/api', '/api')
            print("ОТПРАВЛЯЕМЫЙ JSON:", credit_repay_request_middle.model_dump())

            response = requests.post(
                url=url,
                json=credit_repay_request_middle.model_dump(),
                headers=self.headers,
            )

            self.response_speck_middle(response)
            # Проверяем, успешный ли это статус-код (200 или 201
            if response.status_code in [200, 201]:
                return CreditResponseMiddle(**response.json())
            else:
                # Если это 400, 404 и т.д., возвращаем сам response, чтобы тест не падал на Pydantic-валидации
                return response
