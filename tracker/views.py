from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, authenticate
from django.shortcuts import render, redirect

from .forms import SignUpForm
from .models import get_user_balance, UserProfile


def home(request):
    return render(request, 'home.html')


@login_required
def portfolio(request):
    user = UserProfile.objects.get(user=request.user)
    fiat_symbol = user.fiat.symbol
    balance = get_user_balance(user)
    holdings = 0
    amounts_fiat = []
    for amount_dict in balance.values():
        amounts_fiat.append(amount_dict['amount_fiat'])
    for val in balance.values():
        holdings += val['amount_fiat']
    symbols = [crypto.symbol for crypto in list(balance.keys())]

    colors = ['#114B5F', '#1A936F', '#88D498', '#C6DABF', '#F3E9D2', '#EF5B5B', '#20A39E', '#FFBA49']
    context = {'balance': balance,
               'fiat_symbol': fiat_symbol,
               'holdings': holdings,
               'amounts_fiat': amounts_fiat,
               'symbols': symbols,
               'colors': colors}
    return render(request, 'portfolio.html', context)


@login_required
def settings(request):
    return render(request, 'settings.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            auth_login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})
