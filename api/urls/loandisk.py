from django.urls import path
from api.views import loandisk as view

app_name = 'loandisk'
urlpatterns = [
    path('borrower/<borrower_id>/', view.BorrowerView.as_view(), name='borrower'),
    path('borrower/', view.BorrowerView.as_view(), name='borrower_update'),

    # Loan Routes
    path(
        'loan/borrower/<borrower_id>/from/<page_number>/count/<result_count>/', view.BorrowerLoanListView.as_view(),
        name='borrower_loan_list'
    ),
    path('loan/<loan_id>/', view.LoanDetailView.as_view(), name='loan_detail_by_id'),
    path(
        'loan/loan_application_id/<loan_application_id>/', view.LoanDetailView.as_view(), name="loan_detail_by_app_id"
    ),
    path(
        'loan/adjusted_loan_schedule/<loan_id>/from/<page_number>/count/<result_count>/',
        view.AdjustedLoanScheduleView.as_view(), name='adjusted_loan_schedule'
    ),
    path(
        'loan/original_loan_schedule/<loan_id>/from/<page_number>/count/<result_count>/',
        view.AdjustedLoanScheduleView.as_view(), name='original_loan_schedule'
    ),

    # Loan Repayment
    path('repayment/<repayment_id>/', view.RepaymentDetailView.as_view(), name='repayment_details'),
    path(
        'repayment/loan/<loan_id>/from/<page_number>/count/<result_count>/', view.RepaymentListView.as_view(),
        name="repayment_list"
    ),

    # Savings Products
    path('saving/<savings_id>/', view.SavingsProductDetail.as_view(), name='saving_product_details'),
    path(
        'saving/borrower/<borrower_id>/from/<page_number>/count/<result_count>/', view.SavingsProductList.as_view(),
        name="savings_product_list"
    ),
    path('saving/', view.SavingsProductView.as_view(), name='saving_product'),

    # Savings Transactions
    path('saving_transaction/<transaction_id>/', view.TransactionDetailsView.as_view(), name='transaction_details'),
    path(
        'saving_transaction/saving/<savings_id>/from/<page_number>/count/<result_count>/',
        view.SavingsProductTransactionListView.as_view(), name='savings_product_transaction_list'
    )
]

