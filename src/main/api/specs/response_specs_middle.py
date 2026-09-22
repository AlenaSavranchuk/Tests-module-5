from requests import Response
from http import HTTPStatus


class ResponseSpecs:
    # методы, которые проверяют статус-коды
    @staticmethod
    def request_ok():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.OK, response.text # тут это равно 200 значение ок
        return confirm


    @staticmethod
    def request_created():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.CREATED, response.text # тут значение CREATED = 201
        return confirm

    @staticmethod
    def request_bad():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.BAD_REQUEST
        return confirm

    @staticmethod
    def request_validation_error():
        def confirm(response: Response):
            assert response.status_code in [422,403], response.text

        return confirm

    @staticmethod
    def request_not_found():
        def confirm(response: Response):
            assert response.status_code in [404,403], response.text

        return confirm

    @staticmethod
    def request_unauthorized():
        def confirm(response: Response):
            assert response.status_code == 401, response.text

        return confirm