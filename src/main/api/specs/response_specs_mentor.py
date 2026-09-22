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
            assert response.status_code == HTTPStatus.BAD_REQUEST, response.text
        return confirm