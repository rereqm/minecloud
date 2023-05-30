from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import ModelForm
from main.models import *
from main.forms_utils import *


class CreateServerFrom(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter server name'}), max_length=15)
    plan = forms.ChoiceField(
        label='plan', choices=CHOICES_PLAN)


class SetServerSettingsForm(forms.Form):
    max_players = forms.CharField(label='max_players', initial='20')
    gamemode = forms.ChoiceField(
        label='gamemode', choices=CHOICES_GAMEMODE, initial='survival')
    difficulty = forms.ChoiceField(
        label='difficulty', choices=CHOICES_DIFFICULTY, initial='normal')
    white_list = forms.BooleanField(
        label='white_list', initial=False, required=False)
    online_mode = forms.BooleanField(
        label='online_mode', initial=False, required=False)
    pvp = forms.BooleanField(
        label='pvp', initial=True, required=False)
    allow_flight = forms.BooleanField(
        label='allow_flight', initial=True, required=False)
    spawn_animals = forms.BooleanField(
        label='spawn_animals', initial=True, required=False)
    spawn_monsters = forms.BooleanField(
        label='spawn_monsters', initial=True, required=False)
    spawn_npcs = forms.BooleanField(
        label='spawn_npcs', initial=True, required=False)
    allow_nether = forms.BooleanField(
        label='allow_nether', initial=True, required=False)
    enable_command_block = forms.BooleanField(
        label='command_block', initial=True, required=False)


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label="Login", widget=forms.TextInput(attrs={'placeholder': 'Enter your login'}))
    email = forms.EmailField(label="Email", widget=forms.TextInput(attrs={'placeholder': 'Enter your email'}))
    first_name = forms.CharField(label="Name", widget=forms.TextInput(attrs={'placeholder': 'Enter your name'}))
    last_name = forms.CharField(label="Surname", widget=forms.TextInput(attrs={'placeholder': 'Enter your surname'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}),
                                label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Repeat your password'}),
                                label="Repeat password")

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')  # указываем нужные нам поля


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'placeholder': 'Enter your login'}),
                               max_length=25)
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}))


class SetServerVersionForm(forms.Form):
    version = forms.ChoiceField(
        label='version', choices=CHOICES_VERSION)


class SetModPackForm(forms.Form):
    modpack = forms.ChoiceField(
        label='modpack', choices=CHOICES_MODPACK)


class UserlogoChangeForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['logo_image']


class EmailChangeForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['email']


class UsernameChangeForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username']


class BudgetServerPaymentForm(forms.Form):
    one_day_cost = forms.IntegerField(initial=5, disabled=True)
    days = forms.IntegerField(initial=30)
    total = forms.IntegerField()


class BoostServerPaymentForm(forms.Form):
    one_day_cost = forms.IntegerField(initial=10, disabled=True)
    days = forms.IntegerField(initial=30)
    total = forms.IntegerField()
