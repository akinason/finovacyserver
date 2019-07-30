from django.urls import path
from api import views

app_name = 'loan'
urlpatterns = [
    path('repayment/', views.LoanRepaymentView.as_view(), name='loan_repayment'),
]

