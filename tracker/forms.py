from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from tracker.models import ManualBalance, UserProfile, ExchangeAccount


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ManualBalanceForm(ModelForm):
    class Meta:
        model = ManualBalance
        fields = ('crypto', 'amount')

class ExchangeAccountForm(ModelForm):
    class Meta:
        model = ExchangeAccount
        fields = ('exchange', 'key', 'secret')

class UserProfileFiatForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ('fiat',)
