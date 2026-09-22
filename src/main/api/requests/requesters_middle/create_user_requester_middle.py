import requests
from src.main.api.models.middle.create_user_request_middle import CreateUserRequestMiddle
from src.main.api.models.middle.create_user_response_middle import CreateUserResponseMiddle
from src.main.api.requests.requesters_middle.requester_middle import RequesterMiddle


class CreateUserRequesterMiddle(RequesterMiddle):
    def post(self, create_user_request_middle: CreateUserRequestMiddle):
        url = f'{self.base_url}/api/admin/create'
        response = requests.post(
            url=url,
            json= create_user_request_middle.model_dump(),
            headers=self.headers
        )

        self.response_speck_middle(response)
        return CreateUserResponseMiddle(**response.json())
