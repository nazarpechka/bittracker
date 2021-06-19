from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse

from .models import get_user_balance, UserProfile


def home(request):
    return render(request, 'home.html')


@login_required
def portfolio(request):
    user = UserProfile.objects.get(user=request.user)
    balance = get_user_balance(user)
    holdings = 0
    for val in balance.values():
        holdings += val['amount_fiat']
    return render(request, 'portfolio.html', context={'balance': balance, 'holdings': holdings})


@login_required
def settings(request):
    return render(request, 'settings.html')


@login_required
def logout(request):
    return render(request, 'base.html')


def login(request):
    return render(request, 'base.html')
