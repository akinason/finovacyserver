from decimal import Decimal
import requests

from api.manager import TransactionManager
from api.models import Transaction, TransactionStatus
from finovacyserver import settings

VERSION = 'v2.1'
WIDGET_REQUEST_BASE_URL = "https://api.monetbil.com/widget/{version}/{service_key}"
PAYOUT_BASE_URL = "https://api.monetbil.com/%(version)s/payouts/withdrawal" % {'version': 'v1'}
LOGO_URL = ""
PAYMENT_NOTIFY_URL = "{base_url}{absolute_url}".format(
    base_url=settings.BASE_URL,
    absolute_url="api/transaction/payment/{payment_method}/callback/".format(payment_method="monetbil")
)
PAYOUT_NOTIFY_URL = "{base_url}{absolute_url}".format(
    base_url=settings.BASE_URL,
    absolute_url="api/transaction/payout/{payment_method}/callback/".format(payment_method="monetbil")
)

STANDARD_PHONE_NUMBER_LENGTH = 12
MONETBIL_SERVICE_KEY = 'IUQTPgsgejfni20P6NntjVfHkMTe4iuY'
MONETBIL_SECRET_KEY = 'IA7CBtfvsrOXU95jZXsrYybeA1QUzkUALco7xnBdcFzYnb7xicnehZJVkqBUTBdl'


class Monetbil(object):

    def __init__(self, transaction=None):
        self.transaction = transaction
        self.service_key = ''
        self.amount = ''
        self.currency = ''
        self.invoice = ''
        self.phone = ''
        self.locale = ''
        self.operator = ''
        self.country = ''
        self.item_ref = ''
        self.user = ''
        self.first_name = ''
        self.last_name = ''
        self.email = ''
        self.return_url = ''
        self.notify_url = ''
        self.reference = ''
        self.signature = ''

    def send_payment_widget_request(self, transaction):
        self.transaction = transaction
        self.amount = self.transaction.transaction_amount
        self.currency = self.transaction.currency
        self.amount = ("%f" % self.amount).rstrip('0').rstrip('.')
        self.amount = round(Decimal(self.amount), 0)
        self.reference = self.transaction.reference
        self.return_url = self.transaction.return_url
        self.email = self.transaction.transaction_email
        self.signature = self.transaction.uuid

        params = {
            'amount': self.amount, 'currency': self.currency, 'payment_ref': self.reference, 'email': self.email,
            'logo': LOGO_URL,  'return_url': self.return_url, 'notify_url': PAYMENT_NOTIFY_URL, 'sign': self.signature
        }

        url = WIDGET_REQUEST_BASE_URL.format(service_key=MONETBIL_SERVICE_KEY, version=VERSION)
        r = requests.post(url, params)
        response = r.json()
        success = response['success']
        payment_url = response['payment_url']

        self.transaction.third_party_immediate_response = response
        self.transaction.save()

        if success:
            return {"success": True, "url": payment_url}
        else:
            return {"success": False, "error": "Please check the data you provided and try again."}

    def process_client_payment_request_callback(self, request):
        if request.method == "POST":
            data = request.POST
            message = data.get('message')
            status = data.get('status')
            reference = data.get('payment_ref')
            amount = data.get('amount')
            currency = data.get('currency')
            transaction_id = data.get('transaction_id')

            try:
                self.transaction = Transaction.objects.get(reference=reference)
            except Exception:
                return False
            transaction_status = TransactionStatus()

            if str(status) == '1':
                if self.transaction.server_transaction_status == transaction_status.submitted():
                    self.transaction.third_party_callback_response = data
                    self.transaction.third_party_reference = transaction_id
                    self.transaction.server_transaction_status = transaction_status.paid()
                    self.transaction.save()
                    manager = TransactionManager(transaction=self.transaction)
                    manager.complete_successful_transaction()
                    return True
            else:
                if self.transaction.server_transaction_status == transaction_status.submitted():
                    self.transaction.third_party_callback_response = data
                    self.transaction.save()
                    manager = TransactionManager(transaction=self.transaction)
                    manager.complete_failed_transaction()
                    return True
        else:
            return False

    def process_cash_withdrawal(self, transaction):
        self.transaction = transaction
        """
        Before getting here, we assume that the transaction has already been deducted from the user's loandisk account
        """

        params = {
            'amount': self.transaction.transaction_amount,
            'phonenumber': transaction.borrower_mobile.replace('+', "").replace(" ", ""),
            'processing_number': transaction.reference, 'service_key': MONETBIL_SERVICE_KEY,
            'service_secret': MONETBIL_SECRET_KEY,
            'payout_notification_url': PAYOUT_NOTIFY_URL
        }
        r = requests.post(PAYOUT_BASE_URL, params)
        response = r.json()
        self.transaction.third_party_callback_response = response
        self.transaction.third_party_reference = str(response.get('transaction', 0))
        self.transaction.save()
        manager = TransactionManager(transaction=self.transaction)
        if response.get('success'):
            manager.complete_successful_transaction()
            return {"success": True, "message": response.get('message')}
        else:
            manager.complete_failed_transaction()
            return {"success": False, "message": response.get('message')}
