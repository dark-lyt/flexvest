
from django.urls import path, include
from core.views import  fund_account, home, my_referrals, product, add_to_cart, about, faq, dashboard, withdraw
from django.conf.urls.static import static
from django.conf import settings


app_name = "core"
urlpatterns = [
    path('', home, name="home"),
    path('about/', about, name="about"),
    path('my-dashboard/', dashboard, name="dashboard"),
    path('my-referrals/', my_referrals, name="my_referrals"),
    path('withdraw/', withdraw, name="withdraw"),
    path('fund-account/', fund_account, name="fund_account"),
    path('FAQ/', faq, name="faq"),
    path('product/<slug>/', product, name='product'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),

]

