from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('portfolio', views.portfolio, name='portfolio'),
    path('settings', views.settings, name='settings'),
    path('settings/add_manual_balance', views.add_manual_balance, name='add_manual_balance'),
    path('settings/add_exchange_account', views.add_exchange_account, name='add_exchange_account'),
    path('settings/delete_manual_balance/<int:pk>', views.delete_manual_balance, name='delete_manual_balance'),
    path('settings/delete_exchange_account/<int:pk>', views.delete_exchange_account, name='delete_exchange_account'),
    path('accounts/signup', views.signup, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
]