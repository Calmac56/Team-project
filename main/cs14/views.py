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
    if request.user.is_authenticated:
        return redirect('cs14:index')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                theuser = form.save(commit=False)
                theuser.username = form.cleaned_data.get('email')
                password = User.objects.make_random_password()
                print(theuser.username)
                print(password)
                theuser.set_password(password)
                user = form.cleaned_data.get('email')
                messages.success(request, 'Account was created for ' + user)
               
                home = 'http://127.0.0.1:8000/'
                
                theuser.save()
                user2 = User.objects.get(username=user)
                uniquelink = get_query_string(user2)
                link = home + uniquelink
                themessage = 'Username: ' + theuser.username + '\nPassword: ' + password + '\nUnique login link:' + link
                userstring = str(user)
                send_mail(
                    'User account created for avaloq',
                    themessage,
                    'register@avaloq.com',
                    [userstring],
                    fail_silently=False,

                )
                
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

