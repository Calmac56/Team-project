from django.shortcuts import render, redirect
from django.http import HttpResponse
from static.python.compile import *
from django.contrib.auth.forms import UserCreationForm
from cs14.forms import CreateUserForm, CreateLoginLink
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
<<<<<<< HEAD
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import os
=======
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from sesame.utils import get_query_string
from django.core.mail import send_mail
from cs14.models import Candidate, Admin
>>>>>>> 42e1dfa6f571d708329980da30d34a2088687382

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
    try:
        if request.user.is_authenticated:
            auser = Admin.objects.get(user=request.user)
        else:
            auser = None
    except Admin.DoesNotExist:
        auser = None

    if auser != None:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                theuser = form.save(commit=False)
                theuser.username = form.cleaned_data.get('email')
                password = User.objects.make_random_password()
                theuser.set_password(password)
                username = form.cleaned_data.get('email')
                messages.success(request, 'Account was created for ' + username)
                home = 'http://127.0.0.1:8000/'
                theuser.save()
                user = User.objects.get(username=username)
                thecanditate = Candidate.objects.get_or_create(user=user, first_name=user.first_name, last_name=user.last_name)
                uniquelink = get_query_string(user)
                link = home + uniquelink
                themessage = 'Dear ' + theuser.first_name + '\n' + 'An avaloq coding test account has been created for you with following credentials\n' + 'Username: ' + theuser.username + '\nPassword: ' + password + '\nUnique login link: ' + link + "\nUnique login link is valid for 2 weeks"
                send_mail(
                    'User account created for avaloq',
                    themessage,
                    'avaloqt@gmail.com',
                    [str(username)],
                    fail_silently=False,

                )
                
                return redirect('cs14:register')
    else:
        return redirect('cs14:index')

        
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

