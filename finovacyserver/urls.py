"""finovacyserver URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
import environment

urlpatterns = [
    url('^api/', include('api.urls')),
    url(r'^admin/', admin.site.urls),

]


if environment.env() == environment.DEVELOPMENT:
    from finovacyserver.settings import development
    from django.conf.urls.static import static

    urlpatterns += static(development.STATIC_URL, document_root=development.STATIC_ROOT)
    urlpatterns += static(development.MEDIA_URL, document_root=development.MEDIA_ROOT)
