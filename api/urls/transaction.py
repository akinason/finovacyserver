from django.urls import path
from api import views

app_name = 'transaction'
urlpatterns = [
    path('deposit/', views.DepositView.as_view(), name='deposit'),
    path('withdraw/', views.WithdrawalView.as_view(), name='withdraw'),
    path('/payment/<payment_method>/callback/', views.PaymentCallbackView.as_view(), name='payment_callback'),
    path('/payout/<payment_method>/callback/', views.PaymentCallbackView.as_view(), name='payout_callback'),
]
