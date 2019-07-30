from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import BorrowerManager, Borrower, Transaction
from api.lib.loandisk import Borrower as LoandiskBorrower, LoandiskBase, SavingTransaction as LoandiskSavingTransaction

borrower_manager = BorrowerManager()
branch_id = 9903
email = 'gloxongp@gmail.com'


# class AuthenticationTest(APITestCase):
#
#     def setUp(self):
#         pass
#
#     def test_cannot_create_borrower_with_incomplete_data(self):
#         """
#         Ensure we cannot create a borrower account if the data supplied is not sufficient.
#         """
#         url = reverse('api:auth:signup')
#
#         data = {
#             "borrower_firstname": "Anym", "borrower_lastname": "Simon Tah", "borrower_email": email,
#             "borrower_mobile": "675397307", "borrower_country": "CM"
#         }
#         res = self.client.post(url, data, format='json')
#         self.assertEqual(res.status_code, status.HTTP_206_PARTIAL_CONTENT)
#         self.assertEqual(res.json()['success'], False)
#         self.assertTrue(len(res.json()['errors']) > 0)
#         self.assertTrue(len(res.json()['results']) == 0)
#
#     def test_can_create_borrower_with_complete_data(self):
#         """
#         Ensure we cannot create a borrower account if the data supplied is not sufficient.
#         """
#         url = reverse('api:auth:signup')
#
#         data = {
#             "borrower_firstname": "Anym", "borrower_lastname": "Simon Tah", "borrower_email": email,
#             "borrower_mobile": "675397307", "borrower_country": "CM", "branch_id": branch_id,
#         }
#         res = self.client.post(url, data, format='json')
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.json()['success'], True)  # This test can fail if the email already exist in Loandisk.
#         self.assertTrue(len(res.json()['errors']) == 0)
#         self.assertTrue(len(res.json()['results']) > 0)
#
#         # Delete the borrower account from loandisk and the server to avoid errors in other tests.
#         borrower = Borrower.objects.get(borrower_id=res.json().get('results').get('borrower_id'))
#         borrower.delete()
#
#         loandisk = LoandiskBorrower(branch_id)
#         response = loandisk.delete_borrower(res.json().get('results').get('borrower_id'))
#         self.assertEqual(response.get('response'), 'deleted')
#
#     def test_borrower_can_successfully_reset_password_after_signup(self):
#
#         # First let's create a borrower account, hoping the email does not already exist at loandisk.
#
#         url = reverse('api:auth:signup')
#
#         data = {
#             "borrower_firstname": "Anym", "borrower_lastname": "Simon Tah", "borrower_email": email,
#             "borrower_mobile": "675397307", "borrower_country": "CM", "branch_id": branch_id,
#         }
#         res = self.client.post(url, data, format='json')
#
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.json()['success'], True)
#
#         borrower = Borrower.objects.get(email=email, branch_id=branch_id)
#
#         url = reverse('api:auth:password_reset_confirm')
#         data = {
#             'borrower_id': borrower.borrower_id, 'code': borrower.code, 'branch_id': branch_id, 'new_password': 12345678
#         }
#         res = self.client.post(url, data, format='json')
#
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.json()['success'], True)
#
#         # Delete the borrower account from loandisk and the server to avoid errors in other tests.
#         borrower = Borrower.objects.get(borrower_id=res.json().get('results').get('borrower_id'))
#         borrower.delete()
#
#         loandisk = LoandiskBorrower(branch_id)
#         response = loandisk.delete_borrower(res.json().get('results').get('borrower_id'))
#         self.assertEqual(response.get('response'), 'deleted')
#
#     def test_can_delete_borrower_at_loandisk(self):
#         url = reverse('api:auth:signup')
#
#         data = {
#             "borrower_firstname": "Anym", "borrower_lastname": "Simon Tah", "borrower_email": email,
#             "borrower_mobile": "675397307", "borrower_country": "CM", "branch_id": branch_id,
#         }
#         res = self.client.post(url, data, format='json')
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.json()['success'], True)
#
#         # Delete the borrower account from loandisk and the server to avoid errors in other tests.
#         borrower = Borrower.objects.get(borrower_id=res.json().get('results').get('borrower_id'))
#         borrower.delete()
#
#         loandisk = LoandiskBorrower(branch_id)
#         response = loandisk.delete_borrower(res.json().get('results').get('borrower_id'))
#         self.assertEqual(response.get('response'), 'deleted')
#
#     def test_borrower_can_login_with_email_and_password(self):
#         # First let's create a borrower account, hoping the email does not already exist at loandisk.
#
#         url = reverse('api:auth:signup')
#
#         data = {
#             "borrower_firstname": "Anym", "borrower_lastname": "Simon Tah", "borrower_email": email,
#             "borrower_mobile": "675397307", "borrower_country": "CM", "branch_id": branch_id,
#         }
#         res = self.client.post(url, data, format='json')
#
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.json()['success'], True)
#
#         borrower = Borrower.objects.get(email=email, branch_id=branch_id)
#
#         url = reverse('api:auth:password_reset_confirm')
#         data = {
#             'borrower_id': borrower.borrower_id, 'code': borrower.code, 'branch_id': branch_id, 'new_password': 12345678
#         }
#         res = self.client.post(url, data, format='json')
#
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.json()['success'], True)
#
#         # Delete the borrower account from loandisk to avoid errors in other tests.
#         loandisk = LoandiskBorrower(branch_id)
#         response = loandisk.delete_borrower(res.json().get('results').get('borrower_id'))
#         self.assertEqual(response.get('response'), 'deleted')
#
#         # Login the user.
#         data = {"branch_id": branch_id, "username": email, "password": 12345678}
#         url = reverse("api:auth:login")
#         response = self.client.post(url, data, format='json')
#
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.json()['success'], True)
#         # self.assertContains(res.json().get('results'), 'token')
#
#         # Delete the borrower account from the server to avoid errors in other tests.
#         borrower = Borrower.objects.get(borrower_id=res.json().get('results').get('borrower_id'))
#         borrower.delete()
#
#     def test_borrower_can_login_with_phone_number_and_password(self):
#         # First let's create a borrower account, hoping the email does not already exist at loandisk.
#
#         url = reverse('api:auth:signup')
#
#         data = {
#             "borrower_firstname": "Anym", "borrower_lastname": "Simon Tah", "borrower_email": email,
#             "borrower_mobile": "675397307", "borrower_country": "CM", "branch_id": branch_id,
#         }
#         res = self.client.post(url, data, format='json')
#
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.json()['success'], True)
#
#         borrower = Borrower.objects.get(email=email, branch_id=branch_id)
#
#         url = reverse('api:auth:password_reset_confirm')
#         data = {
#             'borrower_id': borrower.borrower_id, 'code': borrower.code, 'branch_id': branch_id,
#             'new_password': 12345678
#         }
#         res = self.client.post(url, data, format='json')
#
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.json()['success'], True)
#
#         # Delete the borrower account from loandisk to avoid errors in other tests.
#         loandisk = LoandiskBorrower(branch_id)
#         response = loandisk.delete_borrower(res.json().get('results').get('borrower_id'))
#         self.assertEqual(response.get('response'), 'deleted')
#
#         # Login the user.
#         data = {"branch_id": branch_id, "username": "675397307", "password": 12345678}
#         url = reverse("api:auth:login")
#         response = self.client.post(url, data, format='json')
#
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.json()['success'], True)
#         # self.assertContains(res.json().get('results'), 'token')
#
#         # Delete the borrower account from the server to avoid errors in other tests.
#         borrower = Borrower.objects.get(borrower_id=res.json().get('results').get('borrower_id'))
#         borrower.delete()


class TransactionTest(APITestCase):
    #
    # def test_can_deposit_money_into_savings_account(self):
    #     # First let's create a borrower account, hoping the email does not already exist at loandisk.
    #     import random
    #
    #     url = reverse('api:auth:signup')
    #
    #     data = {
    #         "borrower_firstname": "Anym", "borrower_lastname": "Simon Tah", "borrower_email": email,
    #         "borrower_mobile": "675397307", "borrower_country": "CM", "branch_id": branch_id,
    #     }
    #     signup_res = self.client.post(url, data, format='json')
    #
    #     # Create a Savings Account for the user.
    #     savings_account_data = {
    #         "savings_product_id": 1616, "borrower_id": signup_res.json().get('results').get('borrower_id'),
    #         "savings_account_number": random.randint(1500000, 2000000)
    #     }
    #
    #     loandisk = LoandiskBase(branch_id)
    #     endpoint = '/saving'
    #     savings_account_res = loandisk.post(endpoint, savings_account_data)
    #     savings_id = savings_account_res.get('response').get('savings_id')
    #
    #     url = reverse("api:transaction:deposit")
    #     savings_data = {
    #         "payment_method": "CM_MTNMOBILEMONEY", "transaction_amount": random.randint(5000, 150000),
    #         "borrower_mobile": random.randint(670000000, 679999999), "transaction_description": "Test Deposit",
    #         "borrower_id": signup_res.json().get('results').get('borrower_id'), "branch_id": branch_id,
    #         "savings_id": savings_id
    #     }
    #
    #     savings_response = self.client.post(url, savings_data)
    #     print(savings_response.json())
    #
    #     # Delete the borrower account from loandisk to avoid errors in other tests.
    #     loandisk = LoandiskBorrower(branch_id)
    #     response = loandisk.delete_borrower(signup_res.json().get('results').get('borrower_id'))
    #     self.assertEqual(response.get('response'), 'deleted')
    #
    #     # Delete the borrower account from the server to avoid errors in other tests.
    #     borrower = Borrower.objects.get(borrower_id=signup_res.json().get('results').get('borrower_id'))
    #     borrower.delete()

    def test_can_initiate_a_withdrawal_from_savings_account_with_sufficient_funds(self):
        # First let's create a borrower account, hoping the email does not already exist at loandisk.
        import random

        url = reverse('api:auth:signup')

        data = {
            "borrower_firstname": "Anym", "borrower_lastname": "Simon Tah", "borrower_email": email,
            "borrower_mobile": "675397307", "borrower_country": "CM", "branch_id": branch_id,
        }
        signup_res = self.client.post(url, data, format='json')

        borrower = Borrower.objects.get(email=email, branch_id=branch_id)
        url = reverse('api:auth:password_reset_confirm')
        data = {
            'borrower_id': borrower.borrower_id, 'code': borrower.code, 'branch_id': branch_id, 'new_password': 12345678
        }
        res = self.client.post(url, data, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json()['success'], True)

        # Login the user.
        data = {"branch_id": branch_id, "username": email, "password": 12345678}
        url = reverse("api:auth:login")
        response = self.client.post(url, data, format='json')
        token = response.json().get('results').get('token')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        # Create a Savings Account for the user.
        savings_account_data = {
            "savings_product_id": 1616, "borrower_id": signup_res.json().get('results').get('borrower_id'),
            "savings_account_number": random.randint(1500000, 2000000)
        }

        loandisk = LoandiskBase(branch_id)
        endpoint = '/saving'
        savings_account_res = loandisk.post(endpoint, savings_account_data)
        savings_id = savings_account_res.get('response').get('savings_id')

        # Deposit some money in the person's account.
        savings_data = {
             "transaction_amount": 150000, "transaction_description": "Test Deposit",
             "savings_id": savings_id
        }

        loandisk = LoandiskSavingTransaction(branch_id)
        savings_response = loandisk.deposit(savings_data)

        url = reverse("api:transaction:withdraw")
        withdrawal_data = {
            "payment_method": "CM_MTNMOBILEMONEY", "transaction_amount": 10,
            "borrower_mobile": 237675397307, "transaction_description": "Test Deposit",
            "borrower_id": signup_res.json().get('results').get('borrower_id'), "branch_id": branch_id,
            "savings_id": savings_id
        }

        withdrawal_response = self.client.post(url, withdrawal_data)
        self.assertEqual(withdrawal_response.json().get('success'), True)

        # Delete the borrower account from loandisk to avoid errors in other tests.
        loandisk = LoandiskBorrower(branch_id)
        response = loandisk.delete_borrower(signup_res.json().get('results').get('borrower_id'))
        self.assertEqual(response.get('response'), 'deleted')

        # Delete the borrower account from the server to avoid errors in other tests.
        borrower = Borrower.objects.get(borrower_id=signup_res.json().get('results').get('borrower_id'))
        borrower.delete()

    # def test_cannot_initiate_a_withdrawal_from_savings_account_with_insufficient_funds(self):
    #     # First let's create a borrower account, hoping the email does not already exist at loandisk.
    #     import random
    #
    #     url = reverse('api:auth:signup')
    #
    #     data = {
    #         "borrower_firstname": "Anym", "borrower_lastname": "Simon Tah", "borrower_email": email,
    #         "borrower_mobile": "675397307", "borrower_country": "CM", "branch_id": branch_id,
    #     }
    #     signup_res = self.client.post(url, data, format='json')
    #
    #     # Create a Savings Account for the user.
    #     savings_account_data = {
    #         "savings_product_id": 1616, "borrower_id": signup_res.json().get('results').get('borrower_id'),
    #         "savings_account_number": random.randint(1500000, 2000000)
    #     }
    #
    #     loandisk = LoandiskBase(branch_id)
    #     endpoint = '/saving'
    #     savings_account_res = loandisk.post(endpoint, savings_account_data)
    #     savings_id = savings_account_res.get('response').get('savings_id')
    #
    #     """Without a deposit, we assume that the user will not have a balance."""
    #     # savings_data = {
    #     #      "transaction_amount": 150000, "transaction_description": "Test Deposit",
    #     #      "savings_id": savings_id
    #     # }
    #     #
    #     # loandisk = LoandiskSavingTransaction(branch_id)
    #     # savings_response = loandisk.deposit(savings_data)
    #
    #     url = reverse("api:transaction:withdraw")
    #     withdrawal_data = {
    #         "payment_method": "CM_MTNMOBILEMONEY", "transaction_amount": 130000,
    #         "borrower_mobile": random.randint(670000000, 679999999), "transaction_description": "Test Deposit",
    #         "borrower_id": signup_res.json().get('results').get('borrower_id'), "branch_id": branch_id,
    #         "savings_id": savings_id
    #     }
    #     withdrawal_response = self.client.post(url, withdrawal_data)
    #     self.assertEqual(withdrawal_response.json().get('success'), False)
    #
    #     # Delete the borrower account from loandisk to avoid errors in other tests.
    #     loandisk = LoandiskBorrower(branch_id)
    #     response = loandisk.delete_borrower(signup_res.json().get('results').get('borrower_id'))
    #     self.assertEqual(response.get('response'), 'deleted')
    #
    #     # Delete the borrower account from the server to avoid errors in other tests.
    #     borrower = Borrower.objects.get(borrower_id=signup_res.json().get('results').get('borrower_id'))
    #     borrower.delete()
    #
