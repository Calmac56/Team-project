from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.db import models
from .models import *


class CreateUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].required = False
        self.fields['password2'].required = False
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists() or User.objects.filter(username=self.cleaned_data['email']).exists():
            raise forms.ValidationError("Email already in use")

        return self.cleaned_data['email']
     
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

class CreateLoginLink():
    class Meta:
        fields = ['username', 'time']