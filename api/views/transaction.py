from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from api.serializers import transaction_serializer

from api.models import transaction_type, transaction_status
from api.lib.loandisk import SavingTransaction
from api.utils.formating import format_api_response

from api.lib.monetbil import Monetbil


class DepositView(APIView):

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


class PaymentCallbackView(APIView):
    # This view handles payment transactions callbacks emitted by payment processing companies.

    def post(self, request, *args, **kwargs):
        payment_method = kwargs.get('payment_method')

        if payment_method == 'monetbil':
            monetbil = Monetbil()
            monetbil.process_client_payment_request_callback(request)
            return Response({"received": True}, status=status.HTTP_200_OK, content_type='application/json')

    def get(self, request, *args, **kwargs):
        pass
