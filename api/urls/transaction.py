from django.urls import path
from api.views import transaction as view


app_name = 'transaction'
urlpatterns = [
    path('deposit/', view.DepositView.as_view(), name='deposit'),
    path('withdraw/', view.WithdrawalView.as_view(), name='withdraw'),
    path('payment/<payment_method>/callback/', view.PaymentCallbackView.as_view(), name='payment_callback'),
    path('payout/<payment_method>/callback/', view.PaymentCallbackView.as_view(), name='payout_callback'),
]
