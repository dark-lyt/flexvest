from django.urls import path, include
from django.contrib.auth import views as auth_views
from account import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "account"

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('edit/', views.edit, name='edit'),
    path('my-profile/', views.my_profile, name='my_profile'),
    path('signup/', views.register, name='signup'),
    path('mylink/<str:ref_code>/', views.getRecProfile, name='get_profile'),
    path('login/', views.user_login, name='login'),
]
