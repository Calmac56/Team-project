from django.shortcuts import render, redirect
from django.http import HttpResponse
from static.python.compile import * #compilation functions
from django.contrib.auth.forms import UserCreationForm
from cs14.forms import CreateUserForm, CreateLoginLink
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from sesame.utils import get_query_string
from django.core.mail import send_mail
from cs14.models import Candidate, Admin, Results, Reviewer, Task

import datetime
import os
import shutil

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

            userObj = User.objects.get(username=request.user)
            candidate = Candidate.objects.get(user=userObj)

            username = request.user.get_username()
            language = request.POST.get('language').lower()
            submission = request.POST.get('submission')
            print(language)
            filename = 'main'
            testname = 'test1'

            if language == 'python':
                filename += '.py'
            elif language == 'java':
                filename+= '.java'
            print(request.POST.get('codeArea'))

            filepath = os.path.join(USER_DIR, username, testname)

            try:
                os.makedirs(os.path.join(filepath, 'history'))
            except FileExistsError:
                pass
            with open(os.path.join(filepath, filename), 'w+') as f:
                f.write(request.POST.get('codeArea').strip().replace(chr(160), " "))

            results_output, passes, fails = test(testname, username, language)
            

        else:
            return None
    
        return_text = ""
        print(results_output)
        print("Tests passed: ", passes)
        print("Tests failed: ", fails)

        #Store test results in DB
        if submission:
            # ----------------------READ----------------------------------------------
            # still need to properly add complexity, passpercentage, time taken (timer), code
            # current values are for test purposes
            testTask = Task.objects.get(taskID=1)

            if Results.objects.filter(userID=candidate, taskID=testTask):
                pass
            else:
                Results.objects.create(userID=candidate, passpercentage =0, taskID=testTask, tests_passed=0, tests_failed=0, timetaken=1, complexity="test", language="test")
            
            Results.objects.filter(userID=candidate, taskID=testTask).update(passpercentage = int(passes/(passes+fails)*100), tests_passed=passes, tests_failed=fails, timetaken=1, complexity="test", language=language)
            
        for result in results_output:
            if type(result) == type(True):
                return_text+= str(result)
            elif type(result) == type("abc"):
                return_text+= str(result)
            else:
                return_text+= str(result.decode("ASCII"))
        return_text += "Tests passed: " + str(passes) + "\n" + "Tests failed: " + str(fails) + "\n"
    print(request.GET.get('codeArea'))
    return HttpResponse(return_text)

def testCode(request):
    results = []
    if(request.method == 'POST'):
        if request.user.is_authenticated:
            USER_DIR = os.path.join(settings.MEDIA_DIR, 'users')
            username = request.session['scandidate']
            language = request.POST.get('language').lower()
            
            
            filename = 'main'
            testname = 'test1'
            if language == 'python':
                filename += '.py'
            elif language == 'java':
                filename+= '.java'
            
            filepath = os.path.join(USER_DIR, username, testname)
            os.makedirs(os.path.join(filepath, 'temp'))
            with open(os.path.join(filepath, 'temp', filename), 'w+') as f:
                f.write(request.POST.get('codeArea').strip().replace(chr(160), " "))
            results = test2(testname, username, language)
            shutil.rmtree(os.path.join(USER_DIR, username, testname, 'temp'))
        else:
            return None
        return_text = ""
        print(results)
        for result in results:
            if type(result) == type(True):
                return_text+= str(result)
            elif type(result) == type("abc"):
                return_text+= str(result)
            else:
                return_text+= str(result.decode("ASCII"))
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
                
                home = 'http://127.0.0.1:8000/'
                theuser.save()
                user = User.objects.get(username=username)
                thecand = Candidate(user=user)
                thecand.save()
                
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

def results(request):

    result = None
    searchcompleted = False

    try:
        if request.user.is_authenticated:
            auser = Reviewer.objects.get(user=request.user)
        else:
            auser = None
    except Reviewer.DoesNotExist:
        auser = None

    if auser == None:
        return redirect('cs14:login')

    if 'search' in request.GET:
        searched  = request.GET['search']
        searchcompleted = True
        try:
            theuser =  User.objects.get(username = searched)
            try:
                candidate = Candidate.objects.get(user = theuser)
                request.session['scandidate'] = request.GET['search']
                result = Results.objects.filter(userID = candidate)
                if not result:
                    result = None

            
            except Candidate.DoesNotExist:
                result = None
           
        except User.DoesNotExist:
            result = None



    return render(request, 'cs14/results.html', {'results':result, 'searched':searchcompleted})

def cresults(request):
    result = None
    
    try:
        if request.user.is_authenticated:
            auser = Candidate.objects.get(user=request.user)
        else:
            auser = None
    except Candidate.DoesNotExist:
        auser = None

    if auser == None:
        return redirect('cs14:login')

  
    searched  = request.user.username
    try:
        theuser =  User.objects.get(username = searched)
        try:
            candidate = Candidate.objects.get(user = theuser)
            
            result = Results.objects.filter(userID = candidate)
            if not result:
                result = None

            
        except Candidate.DoesNotExist:
            result = None
           
    except User.DoesNotExist:
        result = None
    
    return render(request, 'cs14/cresults.html', {'results':result})


def creview(request,id):
   
    
    if request.user.is_authenticated:
        lines = []
        username = request.user.get_username()
        if Candidate.objects.filter(user=User.objects.get(username=username)).exists():
            theresult = Results.objects.filter(userID=Candidate.objects.filter(user=User.objects.get(username=username)).exists(), taskID=id)
            language = theresult[0].language
            USER_DIR = os.path.join(settings.MEDIA_DIR, 'users')
            finaldir = os.path.join(USER_DIR, username)
            finaldir2 = os.path.join(finaldir, 'test1')
            with open(os.path.join(finaldir2, 'main.py'), "r") as f:
                lines = f.readlines()
        elif Reviewer.objects.filter(user=User.objects.get(username=username)).exists():
            username = request.session.get('scandidate')
            theresult = Results.objects.filter(userID=Candidate.objects.filter(user=User.objects.get(username=username)).exists(), taskID=id)
            language = theresult[0].language
            USER_DIR = os.path.join(settings.MEDIA_DIR, 'users')
            finaldir = os.path.join(USER_DIR, username)
            finaldir2 = os.path.join(finaldir, 'test1')
            with open(os.path.join(finaldir2, 'main.py'), "r") as f:
                lines = f.readlines()

        else:
            return redirect('cs14:home')
    
    else:
        return redirect('cs14:login')

                


    return render(request, 'cs14/codereview.html', {'code':lines, 'language': language})

