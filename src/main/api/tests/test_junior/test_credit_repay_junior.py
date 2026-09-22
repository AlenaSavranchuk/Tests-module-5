import requests
import pytest


@pytest.mark.api

class TestCreditRepay:
    url = "http://localhost:4111"
    def test_credit_repay(self, secret_credit_user_with_accounts):
            # сначала создаем кредит
            token_user = secret_credit_user_with_accounts['token_user']
            account_1 = secret_credit_user_with_accounts['account_1']
            credit_request = requests.post(
                url=f'{self.url}/api/credit/request',
                json={
                    "accountId": account_1,
                    "amount": 5000,
                    "termMonths": 12
                },
                headers={
                    "Content-Type": "application/json",
                    "accept": "application/json",
                    "Authorization": f"Bearer {token_user}"
                }

            )

            assert credit_request.status_code == 201
            credit_id = int(credit_request.json()['creditId'])


            # пополняем счет
            popolnenie_deposit_account = requests.post(
                url=f'{self.url}/api/account/deposit',
                json={
                    "accountId": account_1,
                    "amount": 6000
                },
                headers={
                    'accept': 'application/json',
                    'Authorization': f"Bearer {token_user}"
                }
            )

            # проверяем, пополнился ли счет на сумму пополнения
            assert popolnenie_deposit_account.status_code == 200


            # создаем запрос на погашение самого кредита
            credit_repay_request = requests.post(
                url=f'{self.url}/api/credit/repay',
                json={
                    "creditId": credit_id,
                    "accountId": account_1,
                    "amount": 5000
                },
                headers={
                    "Content-Type": "application/json",
                    "accept": "application/json",
                    "Authorization": f"Bearer {token_user}"
                }
            )

            assert credit_repay_request.status_code == 200


    # для негативного теста, тут не хватает денег
    def test_credit_request_invalid(self, secret_credit_user_with_accounts):
            token_user = secret_credit_user_with_accounts['token_user']
            account_1 = secret_credit_user_with_accounts['account_1']
            credit_request_invalid = requests.post(
                url=f'{self.url}/api/credit/request',
                json={
                    "accountId": account_1,
                    "amount": 5000,
                    "termMonths": 12
                },
                headers={
                    "Content-Type": "application/json",
                    "accept": "application/json",
                    "Authorization": f"Bearer {token_user}"
                }

            )

            assert credit_request_invalid.status_code == 201
            credit_id = credit_request_invalid.json()['creditId']

            # создаем запрос на погашение самого кредита
            credit_repay_request_invalid2 = requests.post(
                url=f'{self.url}/api/credit/repay',
                json={
                    "creditId": credit_id,
                    "accountId": account_1,
                    "amount": 1000
                },
                headers={
                    "Content-Type": "application/json",
                    "accept": "application/json",
                    "Authorization": f"Bearer {token_user}"
                }
            )

            assert credit_repay_request_invalid2.status_code == 422

