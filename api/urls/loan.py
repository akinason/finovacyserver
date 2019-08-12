from django.urls import path
from api.views import loan as view

app_name = 'loan'
urlpatterns = [
    path('repayment/', view.LoanRepaymentView.as_view(), name='loan_repayment'),
]

