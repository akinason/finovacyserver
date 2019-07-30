from django.urls import path
from api.views import IndexView, SignupView, LoginView, PasswordResetView, PasswordResetConfirmView
app_name = 'auth'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('passwordreset/', PasswordResetView.as_view(), name='password_reset'),
    path('passwordreset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm')
]
