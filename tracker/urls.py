from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('portfolio', views.portfolio, name='portfolio'),
    path('settings', views.settings, name='settings'),
    path('logout', views.logout, name='logout'),
    path('login', views.login, name='login')
]