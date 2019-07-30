from rest_framework import serializers
from api.models import Transaction, PAYMENT_METHODS


class LoanRepaymentSerializer(serializers.Serializer):
    branch_id = serializers.IntegerField()
    borrower_id = serializers.IntegerField()
    loan_id = serializers.IntegerField()
    repayment_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    payment_method = serializers.ChoiceField(choices=PAYMENT_METHODS)
    borrower_mobile = serializers.CharField(max_length=20)
    repayment_description = serializers.CharField(max_length=255, required=False)

    class Meta:
        model = Transaction
        fields = (
            'branch_id', 'borrower_id', 'loan_id', 'repayment_amount', 'borrower_mobile', 'repayment_description'
        )
