from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('portfolio', views.portfolio, name='portfolio'),
    path('settings', views.settings, name='settings'),
    path('accounts/', include('django.contrib.auth.urls')),
]