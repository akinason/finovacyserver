from django.urls import path
from api.views import auth as view
app_name = 'auth'
urlpatterns = [
    path('', view.IndexView.as_view(), name='index'),
    path('signup/', view.SignupView.as_view(), name='signup'),
    path('login/', view.LoginView.as_view(), name='login'),
    path('passwordreset/', view.PasswordResetView.as_view(), name='password_reset'),
    path('passwordreset/confirm/', view.PasswordResetConfirmView.as_view(), name='password_reset_confirm')
]
