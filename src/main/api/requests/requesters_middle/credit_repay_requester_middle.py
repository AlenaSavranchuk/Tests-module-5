import requests
from src.main.api.requests.requesters_middle.requester_middle import RequesterMiddle
from src.main.api.models.middle.credit_repay_request_middle import CreditRepayRequestMiddle
from src.main.api.models.middle.credit_repay_response_middle import CreditRepayResponseMiddle


class CreditRepayRequesterMiddle(RequesterMiddle):
    def post(self, credit_repay_request_middle: CreditRepayRequestMiddle):
        url = f'{self.base_url}/api/credit/repay'
        response = requests.post(
            url=url,
            json=credit_repay_request_middle.model_dump(),
            headers=self.headers
        )

        self.response_speck_middle(response)
        if response.ok:
            return CreditRepayResponseMiddle(**response.json())
        return response

