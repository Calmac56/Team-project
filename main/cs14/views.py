from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from cs14.forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

def index(request):
    return render(request, 'cs14/index.html')

def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('cs14:login')
        
    context = {'form': form}
    return render(request, 'cs14/register.html', context)

def loginPage(request):

    if request.method == 'POST':
       username = request.POST.get('username')
       password = request.POST.get('password')
       user = authenticate(request, username=username, password=password)

       if user is not None:
           login(request, user)
           return redirect('cs14:index')

    context = {}
    return render(request, 'cs14/login.html')
