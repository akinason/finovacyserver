import simplejson as json
import requests

from django.utils import timezone


collectors = {
    "9903": 14475,  # Free Trial Branch: Kimbi Gilbert Ngong
}


class LoandiskBase(object):

    def __init__(self, branch_id):
        super(LoandiskBase, self).__init__()
        self.auth_code = "JutHdHDMwMgTjwtexGSPnJBBG46M5n7PctZUBR5u"
        self.public_key = 8223
        self.base_url = 'https://api.loandisk.com/{public_key}/{branch_id}'.format(
            branch_id=branch_id, public_key=self.public_key
        )
        self.headers = {
            'Authorization': 'Basic {code}'.format(code=self.auth_code),
            'Content-Type': 'application/json'
        }

    def get(self, endpoint, params=None):
        url = "{base_url}{endpoint}".format(base_url=self.base_url, endpoint=endpoint)
        res = requests.get(url=url, params=params, headers=self.headers)
        try:
            return res.json()
        except Exception:
            return res

    def post(self, endpoint, data):
        url = "{base_url}{endpoint}".format(base_url=self.base_url, endpoint=endpoint)
        res = requests.post(url, json.dumps(data), headers=self.headers)

        try:
            return res.json()
        except Exception:
            return res

    def put(self, endpoint, data):
        url = "{base_url}{endpoint}".format(base_url=self.base_url, endpoint=endpoint)
        res = requests.put(url=url, data=data, headers=self.headers)
        try:
            return res.json()
        except Exception:
            return False

    def delete(self, endpoint):
        url = "{base_url}{endpoint}".format(base_url=self.base_url, endpoint=endpoint)
        res = requests.delete(url=url, headers=self.headers)
        try:
            return res.json()
        except Exception:
            return False


class Borrower(LoandiskBase):

    def __init__(self, branch_id):
        super(Borrower, self).__init__(branch_id=branch_id)
        self.base_endpoint = '/borrower'

    def add_borrower(self, data):
        endpoint = self.base_endpoint
        return self.post(endpoint, data)

    def update_borrower(self, data):
        endpoint = self.base_endpoint
        return self.put(endpoint, data)

    def get_borrower(self, borrower_id):
        endpoint = "{base}/{borrower_id}".format(base=self.base_endpoint, borrower_id=borrower_id)
        return self.get(endpoint)

    def get_borrowers(self):
        endpoint = "{base}/from/{page_number}/count/{number_of_results}".format(
            base=self.base_endpoint, page_number=1, number_of_results=100000000
        )
        return self.get(endpoint)

    def delete_borrower(self, borrower_id):
        endpoint = "{base}/{borrower_id}".format(base=self.base_endpoint, borrower_id=borrower_id)
        return self.delete(endpoint)


class SavingTransaction(LoandiskBase):
    def __init__(self, branch_id):
        super(SavingTransaction, self).__init__(branch_id)
        self.base_endpoint = '/saving_transaction'

    def deposit(self, data):
        date = timezone.now()
        data['transaction_type_id'] = 1
        data['transaction_date'] = "{:%d/%m/%Y}".format(date)
        data['transaction_time'] = "{:%I:%M %p}".format(date)
        endpoint = self.base_endpoint
        return self.post(endpoint, data)

    def withdraw(self, data):
        date = timezone.now()
        data['transaction_type_id'] = 2
        data['transaction_date'] = "{:%d/%m/%Y}".format(date)
        data['transaction_time'] = "{:%I:%M %p}".format(date)
        endpoint = self.base_endpoint
        return self.post(endpoint, data)

    def reverse_deposit(self, data):
        date = timezone.now()
        data['transaction_type_id'] = 1
        data['transaction_date'] = "{:%d/%m/%Y}".format(date)
        data['transaction_time'] = "{:%I:%M %p}".format(date)
        if 'transaction_description' not in data:
            data['transaction_description'] = 'Reverse deposit'
        endpoint = self.base_endpoint
        return self.post(endpoint, data)


class LoanTransaction(LoandiskBase):

    def __init__(self, branch_id):
        super(LoanTransaction, self).__init__(branch_id)

    def repay_loan(self, data):
        endpoint = '/repayment'
        data['repayment_collected_date'] = "{:%d/%m/%Y}".format(timezone.now())
        collector_id = collectors.get(str(data.get('branch_id')))
        data['collector_id'] = collector_id
        data["loan_repayment_method_id"] = 44398  # Mobile Money
        if 'repayment_description' not in data:
            data['repayment_description'] = 'Loan Repayment'
        return self.post(endpoint, data)

    def request_loan(self, data):
        endpoint = '/loan'

        return self.post(endpoint, data)

    def get_loan_repayment_methods(self):
        endpoint = '/repayment_method/from/1/count/100'
        return self.get(endpoint)

    def get_collected_by_accounts(self):
        endpoint = '/collector/from/1/count/1000'
        return self.get(endpoint)

    def add_repayment_method(self, data):
        endpoint = '/repayment_method'
        return self.post(endpoint, data)

    def add_collector(self, data):
        endpoint = '/collector'
        return self.post(endpoint, data)