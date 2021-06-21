from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, authenticate
from django.shortcuts import render, redirect, get_object_or_404

from .forms import SignUpForm, ManualBalanceForm, ExchangeAccountForm, UserProfileFiatForm
from .models import get_user_balances, UserProfile, ExchangeAccount, ManualBalance


def home(request):
    return render(request, 'home.html')


@login_required
def portfolio(request):
    profile = UserProfile.objects.get(user=request.user)
    fiat_symbol = profile.fiat.symbol
    balances = get_user_balances(profile)

    crypto_symbols = [crypto.symbol for crypto in balances.keys()]
    amounts_fiat = [amounts_dict['amount_fiat'] for amounts_dict in balances.values()]
    holdings_fiat = sum(amounts_fiat)
    colors = ['#114B5F', '#1A936F', '#88D498', '#C6DABF', '#F3E9D2', '#EF5B5B', '#20A39E', '#FFBA49']

    context = {'fiat_symbol': fiat_symbol,
               'balances': balances,
               'crypto_symbols': crypto_symbols,
               'amounts_fiat': amounts_fiat,
               'holdings_fiat': holdings_fiat,
               'colors': colors}
    return render(request, 'portfolio.html', context)


@login_required
def settings(request):
    profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        fiat_form = UserProfileFiatForm(
            request.POST,
            instance=profile
        )
        if fiat_form.is_valid():
            fiat_form.save()

            return redirect('settings')
    else:
        fiat_form = UserProfileFiatForm(instance=profile)

    exchange_accounts = ExchangeAccount.objects.filter(user=profile)
    manual_balances = ManualBalance.objects.filter(user=profile)

    context = {'fiat_form': fiat_form,
               'exchange_accounts': exchange_accounts,
               'manual_balances': manual_balances}
    return render(request, 'settings.html', context)


@login_required
def add_manual_balance(request):
    if request.method == 'POST':
        form = ManualBalanceForm(request.POST)
        if form.is_valid():
            balance = form.save(commit=False)
            balance.user = UserProfile.objects.get(user=request.user)
            balance.save()

            return redirect('settings')
    else:
        form = ManualBalanceForm()
    return render(request, 'add_manual_balance.html', {'form': form})

@login_required
def add_exchange_account(request):
    if request.method == 'POST':
        form = ExchangeAccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = UserProfile.objects.get(user=request.user)
            account.save()

            return redirect('settings')
    else:
        form = ExchangeAccountForm()
    return render(request, 'add_exchange_account.html', {'form': form})

@login_required
def delete_manual_balance(request, pk):
    balance = get_object_or_404(ManualBalance, pk=pk)
    balance.delete()

    return redirect('settings')


@login_required
def delete_exchange_account(request, pk):
    account = get_object_or_404(ExchangeAccount, pk=pk)
    account.delete()

    return redirect('settings')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            auth_login(request, user)
            return redirect('portfolio')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})
