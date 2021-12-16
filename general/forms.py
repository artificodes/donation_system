from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from allauth.account.forms import SignupForm

class SignUpForm(UserCreationForm):
    #gender = forms.CharField(label='First Name', widget = forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email')
    first_name = forms.CharField(label='First Name', widget = forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Last Name', widget = forms.TextInput(attrs={'class': 'form-control'}))
    # user_id = forms.CharField(widget = forms.HiddenInput(attrs={'class': 'form-control'}),required=False,)
    # user = forms.BooleanField(label='User',required=False)
    # usertype = forms.CharField(label='First Name', widget = forms.TextInput(attrs={'class': 'form-control'})