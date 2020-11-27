from django.shortcuts import render, redirect
from django.http import HttpResponse
from cs14.compile import *
from django.contrib.auth.forms import UserCreationForm
from cs14.forms import CreateUserForm, CreateLoginLink
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from sesame.utils import get_query_string
from django.core.mail import send_mail
from cs14.models import Candidate, Admin

def index(request):
    return render(request, 'cs14/index.html')

def codingPage(request):
    return render(request, 'cs14/codingPage.html')

def sendCode(request):
    if(request.method == 'POST'):

        temp = request.POST.get('codeArea')
        file = open("temp.py", "w")
        file.write(temp)
        file.close()
        
        #run the code and do the tests
        compileCode("temp.py", "python")
        run("temp.py", "python")
        results = test("temp.txt", "testFile1.txt")
        return_text = ""

        if(results):
            return_text = "Passed"
        else:
            return_text = "Fail"

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
        print("No permission")
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

