from django.shortcuts import render, redirect
from django.http import HttpResponse
from static.python.compile import *
from django.contrib.auth.forms import UserCreationForm
from cs14.forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import os

def index(request):
    print(settings.MEDIA_DIR)
    return render(request, 'cs14/index.html')

def codingPage(request):
    return render(request, 'cs14/codingPage.html')
#@csrf_exempt
def sendCode(request):
    results = []
    if(request.method == 'POST'):
        if request.user.is_authenticated:
            USER_DIR = os.path.join(settings.MEDIA_DIR, 'users')
            username = request.user.get_username()
            language = request.POST.get('language').lower()
            print(language)
            filename = 'main'
            testname = 'test1'

            if language == 'python':
                filename += '.py'
            elif language == 'java':
                filename+= '.java'
            print(request.POST.get('codeArea'))
            with open(os.path.join(USER_DIR, username, testname, filename), 'w') as f:
                f.write(request.POST.get('codeArea'))

            results = test(testname, username, language)
        else:
            return None
    
        return_text = ""
        if(all(results)):
            return_text = "Passed"
        else:
            return_text = "Fail"
    print(request.GET.get('codeArea'))
    return HttpResponse(return_text)

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
