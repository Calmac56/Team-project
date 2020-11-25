from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

class CreateUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].required = False
        self.fields['password2'].required = False
     
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

class CreateLoginLink():
    class Meta:
        fields = ['username', 'time']