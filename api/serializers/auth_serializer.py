from rest_framework import serializers


class SignupSerializer(serializers.Serializer):
    branch_id = serializers.IntegerField()
    borrower_firstname = serializers.CharField(max_length=255)
    borrower_lastname = serializers.CharField(max_length=255)
    borrower_gender = serializers.CharField(max_length=10, allow_blank=True, allow_null=True, required=False)
    borrower_country = serializers.CharField(max_length=2)
    borrower_mobile = serializers.CharField(max_length=30)
    borrower_email = serializers.EmailField()


class PasswordResetSerializer(serializers.Serializer):
    borrower_email = serializers.EmailField()
    branch_id = serializers.IntegerField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    borrower_id = serializers.IntegerField()
    code = serializers.IntegerField()
    new_password = serializers.CharField(max_length=150)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=150)
    branch_id = serializers.IntegerField()
