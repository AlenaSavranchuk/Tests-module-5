import requests

from src.main.api.models.middle.transfer_request_middle import TransferRequestMiddle
from src.main.api.models.middle.transfer_response_middle import TransferResponseMiddle
from src.main.api.requests.requesters_middle.requester_middle import RequesterMiddle


class TransferRequesterMiddle(RequesterMiddle):
    def post(self, transfer_request_middle: TransferRequestMiddle):
        url = f'{self.base_url}/api/account/transfer'
        response = requests.post(
            url=url,
            json=transfer_request_middle.model_dump(),
            headers=self.headers
        )

        self.response_speck_middle(response)
        if response.ok:
            return TransferResponseMiddle(**response.json())
        return response