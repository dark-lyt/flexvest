"""flexvest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from cryptocurrency_payment import urls as cryptocurrency_payment_urls
from flexvest.settings import STATIC_ROOT, STATIC_URL

from django.conf.urls.static import static


# path('dashboard/', views.dashboard, name='dashboard'),
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("core.urls", namespace='core')),
    path('', include('django.contrib.auth.urls')),
    path('account/', include("account.urls", namespace='account')),
    path('paydetails/', include(cryptocurrency_payment_urls)),
] + static(STATIC_URL, document_root=STATIC_ROOT)
