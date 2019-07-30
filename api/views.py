from django.contrib.auth import authenticate
from django.views import generic

from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from api.serializers import auth_serializer, transaction_serializer, loan_serializer

from api.models import Borrower as BorrowerModel, BorrowerManager, transaction_type, transaction_status
from api.lib.loandisk import Borrower as LoandiskBorrower, SavingTransaction, LoanTransaction
from api.utils.formating import format_api_response

from api.lib.mailing import send_password_set_or_reset_email
from api.lib.monetbil import Monetbil

borrower_manager = BorrowerManager()


class IndexView(generic.TemplateView):
    template_name = 'api/index.html'


class SignupView(APIView):

    def post(self, request, format=None):
        serializer = auth_serializer.SignupSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            branch_id = data.pop('branch_id', None)
            email = data.get('borrower_email')
            phone = data.get('borrower_mobile')
            loandisk = LoandiskBorrower(branch_id)

            # Be sure the email does not already exist in the selected branch
            if BorrowerModel.objects.filter(email=email, branch_id=branch_id).exists():
                response = format_api_response(success=False, error_message="Email already registered with another account.")
                return Response(response, status=status.HTTP_200_OK)

            # Add the account to loandisk
            res = loandisk.add_borrower(data)

            # Maybe email already exist in loandisk
            if 'Errors' in res.get('response'):
                error = res.get('response').get('Errors')[0]
                response = format_api_response(success=False, error_message=error)
                return Response(response, status=status.HTTP_200_OK)

            # Create a user account for the current borrower
            borrower_id = res.get('response').get('borrower_id')
            borrower = BorrowerModel.objects.create(
                borrower_id=borrower_id, email=email, phone=phone, branch_id=branch_id
            )

            # Send a password reset code to the user's email
            email_response = send_password_set_or_reset_email(email, data.get('borrower_firstname'))

            # Prepare the response.
            result = {"branch_id": branch_id, "borrower_id": borrower_id, "code": email_response.get('code')}
            borrower.code = email_response.get('code')
            borrower.save()

            response = format_api_response(success=True, result=result)
            return Response(response, status=status.HTTP_200_OK)

        response = format_api_response(success=False, errors=serializer.errors)
        return Response(response, status=status.HTTP_206_PARTIAL_CONTENT)


class PasswordResetView(APIView):

    def post(self, request, format=None):
        serializer = auth_serializer.PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('borrower_email')
            branch_id = serializer.data.get('branch_id')
            try:
                borrower = BorrowerModel.objects.get(email=email, branch_id=branch_id)
                res = send_password_set_or_reset_email(email)
                result = {"borrower_id": borrower.borrower_id, "code": res.get('code'), "branch_id": borrower.branch_id}
                response = format_api_response(success=True, result=result)
                return Response(response, status=status.HTTP_200_OK)
            except BorrowerModel.DoesNotExist:
                error_message = "Account with provided credentials does not exist."
                response = format_api_response(success=False, error_message=error_message)
                return Response(response, status=status.HTTP_200_OK)

        response = format_api_response(success=False, errors=serializer.errors)
        return Response(response, status=status.HTTP_206_PARTIAL_CONTENT)


class PasswordResetConfirmView(APIView):

    def post(self, request, format=None):
        serializer = auth_serializer.PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            borrower_id = serializer.data.get('borrower_id')
            password = serializer.data.get('new_password')
            code = serializer.data.get('code')
            try:
                borrower = BorrowerModel.objects.get(borrower_id=borrower_id)
                if code == int(code):
                    borrower.set_password(password)
                    borrower.save()
                    result = {"branch_id": borrower.branch_id, "borrower_id": borrower.borrower_id}
                    response = format_api_response(success=True, result=result)
                    return Response(response, status=status.HTTP_200_OK)
                else:
                    error_message = "Code provided does not exist."
                    response = format_api_response(success=False, error_message=error_message)
                    return Response(response, status=status.HTTP_200_OK)
            except BorrowerModel.DoesNotExist:
                error_message = "Borrower with id {id} does not exist.".format(id=borrower_id)
                response = format_api_response(success=False, error_message=error_message)
                return Response(response, status=status.HTTP_200_OK)

        response = format_api_response(success=False, errors=serializer.errors)
        return Response(response, status=status.HTTP_206_PARTIAL_CONTENT)


class LoginView(APIView):

    def post(self, request, format=None):
        serializer = auth_serializer.LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.data.get('username')
            password = serializer.data.get('password')
            branch_id = serializer.data.get('branch_id')
            is_authenticated = authenticate(request, username=username, password=password, branch_id=branch_id)
            # is_authenticated = True
            if is_authenticated:
                borrower = borrower_manager.get_borrower(branch_id=branch_id, username=username)
                token = Token.objects.create(user=borrower)
                result = {"token": token.key, "borrower_id": borrower.borrower_id, "branch_id": branch_id}
                response = format_api_response(success=True, result=result)
                return Response(response, status=status.HTTP_200_OK)
            else:
                error_message = "Username or Password Incorrect."
                response = format_api_response(success=False, error_message=error_message)
                return Response(response, status=status.HTTP_200_OK)

        response = format_api_response(success=False, errors=serializer.errors)
        return Response(response, status=status.HTTP_206_PARTIAL_CONTENT)


class DepositView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request, format=None):

        serializer = transaction_serializer.TransactionSerializer(data=request.data)
        if serializer.is_valid():

            # Save the transaction
            transaction = serializer.save()
            transaction.server_transaction_type = transaction_type.savings()
            transaction.server_transaction_status = transaction_status.submitted()
            transaction.save()

            # Call the Payment API
            monetbil = Monetbil()
            res = monetbil.send_payment_widget_request(transaction=transaction)

            # Prepare a response to send to the borrower
            if res.get('success'):
                result = {"server_transaction_id": transaction.id, "payment_url": res.get('payment_url')}
                response = format_api_response(success=True, result=result)
                return Response(response, status=status.HTTP_200_OK)
            else:
                transaction.server_transaction_status = transaction_status.failed()
                transaction.is_completed = True
                transaction.save()
                response = format_api_response(success=False, error_message=res.get('error'))
                return Response(response, status=status.HTTP_200_OK)
        response = format_api_response(success=False, errors=serializer.errors)
        return Response(response, status=status.HTTP_206_PARTIAL_CONTENT)


class WithdrawalView(APIView):

    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        serializer = transaction_serializer.TransactionSerializer(data=request.data)
        if serializer.is_valid():

            # Save the transaction
            transaction = serializer.save()
            transaction.server_transaction_type = transaction_type.withdrawal()
            transaction.server_transaction_status = transaction_status.submitted()
            transaction.save()

            # Withdraw the money from the person's account.
            loandisk = SavingTransaction(transaction.branch_id)
            data = {
                "savings_id": transaction.savings_id, "transaction_amount": transaction.transaction_amount,
                "transaction_description": transaction.transaction_description
            }
            loandisk_response = loandisk.withdraw(data=data)

            if 'Errors' in loandisk_response.get('response'):
                # mark transaction in the server as completed.
                transaction.is_completed = True
                transaction.third_party_immediate_response = loandisk_response
                transaction.save()

                errors = loandisk_response.get('response').get('Errors')
                response = format_api_response(success=False, errors=errors)
                return Response(response, status=status.HTTP_200_OK)

            # Call the MoMo Payment API and cash out the money.
            monetbil = Monetbil()
            res = monetbil.process_cash_withdrawal(transaction=transaction)

            # Prepare a response to send to the borrower
            if not res.get('success'):
                response = format_api_response(success=res.get('success'), result={}, error_message=res.get('message'))
                return Response(response, status=status.HTTP_200_OK)
            result = {"server_transaction_id": transaction.id}
            response = format_api_response(success=True, result=result)
            return Response(response, status=status.HTTP_200_OK)
        response = format_api_response(success=False, errors=serializer.errors)
        return Response(response, status=status.HTTP_206_PARTIAL_CONTENT)


class LoanRequestView(APIView):

    def post(self, request, *args, **kwargs):
        pass


class LoanRepaymentView(APIView):

    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = loan_serializer.LoanRepaymentSerializer(data=request.data)
        if serializer.is_valid():
            # Save the data
            transaction = serializer.save()
            transaction.server_transaction_type = transaction_type.loan_repayment()
            transaction.save()

            # Send a Mobile Money Cash out request.
            monetbil = Monetbil()
            res = monetbil.send_payment_widget_request(transaction=transaction)

            # Prepare the response.
            if res.get('success'):
                result = {"server_transaction_id": transaction.id, "payment_url": res.get('payment_url')}
                response = format_api_response(success=True, result=result)
                return Response(response, status=status.HTTP_200_OK)
            else:
                response = format_api_response(success=False, error_message=res.get('message'))
                return Response(response, status=status.HTTP_200_OK)
        response = format_api_response(success=False, errors=serializer.errors)
        return Response(response, status=status.HTTP_206_PARTIAL_CONTENT)
    

class PaymentCallbackView(generic.View):
    # This view handles payment transactions callbacks emitted by payment processing companies.

    def post(self, request, *args, **kwargs):
        payment_method = kwargs.get('payment_method')

        if payment_method == 'monetbil':
            monetbil = Monetbil()
            monetbil.process_client_payment_request_callback(request)
            return {"received": True}

    def get(self, request, *args, **kwargs):
        pass
