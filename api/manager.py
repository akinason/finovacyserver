from api.models import TransactionStatus, TransactionType
from api.lib.loandisk import SavingTransaction, LoanTransaction

transaction_status = TransactionStatus()
transaction_type = TransactionType()


class TransactionManager(object):

    def __init__(self, transaction):
        self.transaction = transaction

    def _deposit(self):
        loandisk = SavingTransaction(branch_id=self.transaction.branch_id)
        data = {
            "savings_id": self.transaction.savings_id, "transaction_amount": self.transaction.transaction_amount,
            "transaction_description": self.transaction.transaction_description
        }
        res = loandisk.deposit(data=data)
        if 'Error' not in res:
            self.transaction.server_transaction_status = transaction_status.completed()
            self.transaction.is_completed = True
            self.transaction.save()
        else:
            self.transaction.server_transaction_status = transaction_status.pending_retry()
            self.transaction.save()
        return res

    def _withdraw(self):
        pass

    def _repay_loan(self):
        data = {
            "loan_id": self.transaction.loan_id, "repayment_amount": self.transaction.repayment_amount
        }
        loandisk = LoanTransaction(branch_id=self.transaction.branch_id)
        res = loandisk.repay_loan(data=data)
        if 'Error' not in res:
            self.transaction.server_transaction_status = transaction_status.completed()
            self.transaction.is_completed = True
            self.transaction.save()
        else:
            self.transaction.server_transaction_status = transaction_status.pending_retry()
            self.transaction.save()

    def _reverse_deposit(self):
        """A deposit meant to reverse a previous withdrawal on a client's account. """
        data = {"savings_id": self.transaction.savings_id, "transaction_amount": self.transaction.transaction_amount}
        loandisk = SavingTransaction(branch_id=self.transaction.branch_id)
        return loandisk.reverse_deposit(data=data)

    def complete_successful_transaction(self):
        """If the transaction is already completed, simply respond with a success status."""
        if self.transaction.server_transaction_status == transaction_status.completed():
            return {"success": True, "transaction_id": self.transaction.id, "message": "Transaction Successful"}

        if self.transaction.server_transaction_type == transaction_type.savings():
            if not self.transaction.server_transaction_status == transaction_status.paid():
                return {"success": False, "message": "This transaction has not yet been paid."}

            return self._deposit()

        if self.transaction.server_transaction_type == transaction_type.loan_repayment():
            if not self.transaction.server_transaction_status == transaction_status.paid():
                return {"success": False, "message": "This transaction has not yet been paid."}

            return self._repay_loan()

        if self.transaction.server_transaction_type == transaction_type.withdrawal():
            """We do no need to call self._withdraw() because the withdrawal at loandisk has already been done."""
            self.transaction.server_transaction_status = transaction_status.completed()
            self.transaction.is_completed = True
            self.transaction.save()
            return {"success": True, "message": "Transaction Successful."}

    def complete_failed_transaction(self):
        if self.transaction.server_transaction_status == transaction_status.submitted():
            self.transaction.server_transaction_status = transaction_status.failed()
            self.transaction.is_completed = True
            self.transaction.save()

            """If the transaction that failed was a withdrawal, reverse the hold on the client's account on loandisk"""
            if self.transaction.server_transaction_type == transaction_type.withdrawal():
                return self._reverse_deposit()
