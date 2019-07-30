from rest_framework import serializers
from api.models import Transaction, PAYMENT_METHODS


class TransactionSerializer(serializers.ModelSerializer):
    branch_id = serializers.IntegerField()
    borrower_id = serializers.IntegerField()
    savings_id = serializers.IntegerField()
    transaction_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    payment_method = serializers.ChoiceField(choices=PAYMENT_METHODS)
    transaction_description = serializers.CharField(required=False, max_length=255)
    borrower_mobile = serializers.CharField(max_length=25)
    transaction_email = serializers.EmailField(max_length=50, required=False)

    class Meta:
        model = Transaction
        fields = (
            'savings_id', 'transaction_amount', 'payment_method', 'transaction_description', 'borrower_mobile',
            'borrower_id', 'branch_id', 'transaction_email'
        )
