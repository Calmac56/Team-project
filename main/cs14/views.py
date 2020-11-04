from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from cs14.forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'cs14/index.html')

def register(request):
    if request.user.is_authenticated:
        return redirect('cs14:index')
    else:
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
    if request.user.is_authenticated:
        return redirect('cs14:index')
    else:
    
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('cs14:index')
            else:
                messages.info(request, 'Username or password is incorrect')

    context = {}
    return render(request, 'cs14/login.html')

def logoutUser(request):
    logout(request)
    return redirect('cs14:login')
