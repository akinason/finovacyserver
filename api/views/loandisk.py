"""
    This is just a passer between the front end application and loandisk.
    This is due to the fact that calling loandisk directly from the front end application
    produces a CORS issue.

    However, this also ensures that all calls from the front end application are done after a user is
    duly authenticated.
"""
import json

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from api.lib.loandisk import LoandiskBase


class BorrowerView(APIView):
    """Uer must have been authenticated to access this route."""

    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        branch_id = request.user.branch_id
        borrower_id = request.user.borrower_id
        loandisk = LoandiskBase(branch_id)
        response = loandisk.get('/borrower/{id}'.format(id=borrower_id))
        return Response(response, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        branch_id = request.user.branch_id
        borrower_id = request.user.borrower_id
        loandisk = LoandiskBase(branch_id)
        response = loandisk.put('/borrower', data=json.dumps(request.data))
        return Response(response, status=status.HTTP_200_OK)


"""
Loan Routes
"""


class LoanDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        application_id = kwargs.get('loan_application_id')
        loan_id = kwargs.get('loan_id')
        branch_id = request.user.branch_id
        loandisk = LoandiskBase(branch_id)
        endpoint = ''
        if application_id:
            endpoint = '/loan/loan_application_id/{id}'.format(id=application_id)
        elif loan_id:
            endpoint = '/loan/{id}'.format(id=loan_id)

        response = loandisk.get(endpoint)
        return Response(response, status=status.HTTP_200_OK)


class BorrowerLoanListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        branch_id = request.user.branch_id
        borrower_id = request.user.borrower_id
        loandisk = LoandiskBase(branch_id)
        page_number = kwargs.get('page_number')
        result_count = kwargs.get('result_count')
        endpoint = '/loan/borrower/{borrower_id}/from/{page_number}/count/{result_count}'.format(
            borrower_id=borrower_id, page_number=page_number, result_count=result_count
        )
        response = loandisk.get(endpoint)
        return Response(response, status=status.HTTP_200_OK)


class OriginalLoanScheduleView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        branch_id = request.user.branch_id
        loandisk = LoandiskBase(branch_id)
        loan_id = kwargs.get('loan_id')
        page_number = kwargs.get('page_number')
        result_count = kwargs.get('result_count')
        endpoint = '/loan/original_loan_schedule/{loan_id}/from/{page_number}/count/{result_count}'.format(
            loan_id=loan_id, page_number=page_number, result_count=result_count
        )
        response = loandisk.get(endpoint)
        return Response(response, status=status.HTTP_200_OK)


class AdjustedLoanScheduleView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        branch_id = request.user.branch_id
        loandisk = LoandiskBase(branch_id)
        loan_id = kwargs.get('loan_id')
        page_number = kwargs.get('page_number')
        result_count = kwargs.get('result_count')
        endpoint = '/loan/adjusted_loan_schedule/{loan_id}/from/{page_number}/count/{result_count}'.format(
            loan_id=loan_id, page_number=page_number, result_count=result_count
        )
        response = loandisk.get(endpoint)
        return Response(response, status=status.HTTP_200_OK)


class RepaymentDetailView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        branch_id = request.user.branch_id
        loandisk = LoandiskBase(branch_id)
        repayment_id = kwargs.get('repayment_id')
        response = loandisk.get('/repayment/{id}'.format(id=repayment_id))
        return Response(response, status=status.HTTP_200_OK)


class RepaymentListView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        branch_id = request.user.branch_id
        loandisk = LoandiskBase(branch_id)
        loan_id = kwargs.get('loan_id')
        page_number = kwargs.get('page_number')
        result_count = kwargs.get('result_count')
        endpoint = '/repayment/loan/{loan_id}/from/{page_number}/count/{result_count}'.format(
            loan_id=loan_id, page_number=page_number, result_count=result_count
        )
        response = loandisk.get(endpoint)
        return Response(response, status=status.HTTP_200_OK)


class SavingsProductDetail(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        branch_id = request.user.branch_id
        loandisk = LoandiskBase(branch_id)
        savings_id = kwargs.get('savings_id')
        response = loandisk.get('/saving/{id}'.format(id=savings_id))
        return Response(response, status=status.HTTP_200_OK)


class SavingsProductList(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        branch_id = request.user.branch_id
        borrower_id = request.user.borrower_id
        loandisk = LoandiskBase(branch_id)
        page_number = kwargs.get('page_number')
        result_count = kwargs.get('result_count')
        endpoint = '/saving/borrower/{borrower_id}/from/{page_number}/count/{result_count}'.format(
            borrower_id=borrower_id, page_number=page_number, result_count=result_count
        )
        response = loandisk.get(endpoint)
        return Response(response, status=status.HTTP_200_OK)


class SavingsProductView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        branch_id = request.user.branch_id
        loandisk = LoandiskBase(branch_id)
        response = loandisk.post('/saving', data=json.dumps(request.data))
        return Response(response, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        branch_id = request.user.branch_id
        loandisk = LoandiskBase(branch_id)
        response = loandisk.put('/saving', data=json.dumps(request.data))
        return Response(response, status=status.HTTP_200_OK)


class TransactionDetailsView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        branch_id = request.user.branch_id
        loandisk = LoandiskBase(branch_id)
        transaction_id = kwargs.get('transaction_id')
        response = loandisk.get('/saving_transaction/{id}'.format(id=transaction_id))
        return Response(response, status=status.HTTP_200_OK)


class SavingsProductTransactionListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        branch_id = request.user.branch_id
        loandisk = LoandiskBase(branch_id)
        page_number = kwargs.get('page_number')
        result_count = kwargs.get('result_count')
        savings_id = kwargs.get('savings_id')
        endpoint = '/saving_transaction/saving/{savings_id}/from/{page_number}/count/{result_count}'.format(
            savings_id=savings_id, page_number=page_number, result_count=result_count
        )
        response = loandisk.get(endpoint)
        return Response(response, status=status.HTTP_200_OK)
