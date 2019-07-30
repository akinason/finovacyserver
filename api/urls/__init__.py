from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'api'
urlpatterns = [
    path('auth/', include('api.urls.auth')),
    path('transaction/', include('api.urls.transaction')),
    path('loan/', include('api.urls.loan')),
]

urlpatterns = format_suffix_patterns(urlpatterns)
