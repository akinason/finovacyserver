import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

import environment

PAYMENT_METHODS = (('CM_MTNMOBILEMONEY', 'CM_MTNMOBILEMONEY'), ('CM_ORANGEMONEY', 'CM_ORANGEMONEY'))


class TransactionType(object):

    def __init__(self):
        self._loan_repayment = 'LOAN_REPAYMENT'
        self._savings = 'SAVINGS'
        self._withdrawal = 'WITHDRAWAL'
        self._loan_request = 'LOAN_REQUEST'

    def loan_repayment(self):
        return self._loan_repayment

    def savings(self):
        return self._savings

    def withdrawal(self):
        return self._withdrawal

    def loan_request(self):
        return self._loan_request


transaction_type = TransactionType()


class TransactionStatus(object):

    def __init__(self):
        self._submitted = 'SUBMITTED'
        self._paid = 'PAID'
        self._completed = "COMPLETED"
        self._failed = 'FAILED'
        self._pending_retry = 'PENDING_RETRY'

    def submitted(self):
        return self._submitted

    def paid(self):
        return self._paid

    def completed(self):
        return self._completed

    def failed(self):
        return self._failed

    def pending_retry(self):
        return self._pending_retry


transaction_status = TransactionStatus()


class BorrowerManager(object):

    def account_exist(self, email, branch_id):
        return Borrower.objects.filter(email=email, branch_id=branch_id).exists()

    def get_borrower(self, **kwargs):

        if 'branch_id' in kwargs:
            if 'email' in kwargs:
                try:
                    return Borrower.objects.get(branch_id=kwargs.get('branch_id'), email=kwargs.get('email'))
                except Exception:
                    pass

            if 'phone' in kwargs:
                try:
                    return Borrower.objects.get(branch_id=kwargs.get('branch_id'), phone=kwargs.get('phone'))
                except Exception:
                    pass

            if 'username' in kwargs:
                try:
                    return Borrower.objects.get(email=kwargs.get('username'), branch_id=kwargs.get('branch_id'))
                except Exception:
                    pass

                try:
                    return Borrower.objects.get(phone=kwargs.get('username'), branch_id=kwargs.get('branch_id'))
                except Exception:
                    pass

        if 'borrower_id' in kwargs:
            try:
                return Borrower.objects.get(borrower_id=kwargs.get('borrower_id'))
            except Exception:
                pass

        return None


class Borrower(AbstractUser):
    borrower_id = models.IntegerField(_('Borrower ID'), unique=True, blank=True, null=True)
    branch_id = models.IntegerField(_('Branch ID'), blank=True, null=True)
    email = models.EmailField(_('Email Address'), blank=True, null=True)
    phone = models.CharField(_('Phone Number'), max_length=255, blank=True)
    password = models.TextField(blank=True, null=True)
    code = models.IntegerField(blank=True, null=True)

    USERNAME_FIELD = 'username'

    class Meta:
        unique_together = (('email', 'branch_id'), )

    def save(self, *args, **kwargs):
        while True:
            username = str(uuid.uuid4())
            if Borrower.objects.filter(username=username).exists():
                pass
            else:
                self.username = username
                break
        self.is_superuser = True
        super(Borrower, self).save(*args, **kwargs)


class Transaction(models.Model):
    branch_id = models.IntegerField(null=True, blank=True)
    borrower_id = models.IntegerField(null=True, blank=True)
    transaction_id = models.IntegerField(null=True, blank=True)
    savings_id = models.IntegerField(null=True, blank=True)
    transaction_date = models.DateField(null=True, blank=True)
    transaction_time = models.TimeField(null=True, blank=True)
    transaction_type_id = models.IntegerField(null=True, blank=True)
    transaction_amount = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)
    transaction_description = models.CharField(blank=True, max_length=255)
    transaction_balance = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)
    transaction_email = models.EmailField(blank=True, null=True)
    currency = models.CharField(max_length=3, default='XAF')
    reference = models.CharField(blank=True, null=True, max_length=255)

    # Specific to loan repayment
    loan_id = models.IntegerField(null=True, blank=True)
    repayment_id = models.IntegerField(null=True, blank=True)
    repayment_description = models.CharField(max_length=255, blank=True)

    payment_method = models.CharField(blank=True, max_length=50, choices=PAYMENT_METHODS)
    borrower_mobile = models.CharField(blank=True, max_length=50)
    server_transaction_status = models.CharField(blank=True, max_length=20)
    is_completed = models.BooleanField(default=False)
    third_party_reference = models.CharField(blank=True, max_length=255)
    third_party_immediate_response = models.TextField(blank=True)
    third_party_callback_response = models.TextField(blank=True)
    return_url = models.CharField(max_length=255, blank=True)
    server_transaction_type = models.CharField(blank=True, max_length=50)
    created_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    submitted_on = models.DateTimeField(auto_now_add=True)
    uuid = models.UUIDField(default=uuid.uuid4())

    def set_reference(self):
        if not self.reference:
            if environment.env() == environment.PRODUCTION:
                self.reference = "FINO.{id}.{env}".format(id=self.pk, env="P")
            else:
                import random
                self.reference = "FINO.{id}.{env}".format(id=random.randint(250, 750000), env="D")

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(Transaction, self).save()
        self.set_reference()
        super(Transaction, self).save()






