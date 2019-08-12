from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from api.serializers import loan_serializer

from api.models import transaction_type
from api.utils.formating import format_api_response

from api.lib.monetbil import Monetbil


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

