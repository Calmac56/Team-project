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
import json

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
            with open(os.path.join(filepath, 'history',str(datetime.datetime.now()) + '.txt'), 'w+') as f:
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
            if Reviewer.objects.filter(user=request.user):
                username = request.session['scandidate']
            else:
                username = request.user.username
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


    try:
        task = Task.objects.filter(taskID=id)
        taskDec = task[0].description
        taskout = task[0].expectedout
    except:
        taskDec = "Could not get task description"
        taskout = "Could not get expected output"


    timelinelength = 0
    
    if request.user.is_authenticated:
        lines = []
        username = request.user.get_username()
        if Candidate.objects.filter(user=User.objects.get(username=username)).exists():
            theresult = Results.objects.filter(userID=Candidate.objects.filter(user=User.objects.get(username=username)).exists(), taskID=id)
            try:
                language = theresult[0].language
            except:
                language = "python"
            try:
                USER_DIR = os.path.join(settings.MEDIA_DIR, 'users')
                finaldir = os.path.join(USER_DIR, username)
                finaldir2 = os.path.join(finaldir, 'test' + str(id))
                historydir = os.path.join(finaldir2, 'history')
                onlyfiles = [f for f in os.listdir(historydir) if os.path.isfile(os.path.join(historydir, f))]
                timelinelength = len(onlyfiles) - 1
                
                
                with open(os.path.join(finaldir2, 'main.py'), "r") as f:
                    lines = f.readlines()
            except FileNotFoundError:
                lines = "The coding file could not be found, backend error"
        elif Reviewer.objects.filter(user=User.objects.get(username=username)).exists():
            username = request.session.get('scandidate')
            theresult = Results.objects.filter(userID=Candidate.objects.filter(user=User.objects.get(username=username)).exists(), taskID=id)
            try:
                language = theresult[0].language
            except:
                language = "python"
            try:
                USER_DIR = os.path.join(settings.MEDIA_DIR, 'users')
                finaldir = os.path.join(USER_DIR, username)
                testname = "test" + str(id)
                finaldir2 = os.path.join(finaldir, testname)
                histdir = os.path.join(finaldir2, 'history')
                onlyfiles = [f for f in os.listdir(histdir) if os.path.isfile(os.path.join(histdir, f))]
                timelinelength = len(onlyfiles) - 1
                with open(os.path.join(finaldir2, 'main.py'), "r") as f:
                    lines = f.readlines()
            except FileNotFoundError:
                lines = "The coding file could not be found, backend error"

        else:
            return redirect('cs14:home')
    
    else:
        return redirect('cs14:login')

                


    return render(request, 'cs14/codereview.html', {'code':lines, 'language': language , 'taskDec':taskDec, 'taskout':taskout, 'slideval':timelinelength, 'taskID':id})


def rhistory(request):
    lines = []
   
    if(request.method == 'POST'):
        if request.user.is_authenticated:
            username = request.user.get_username()
            value = request.POST.get("number")
            id  = request.POST.get("taskID")
     
            
            if Candidate.objects.filter(user=User.objects.get(username=username)).exists():
                
                try:
                    USER_DIR = os.path.join(settings.MEDIA_DIR, 'users')
                    finaldir = os.path.join(USER_DIR, username)
                    finaldir2 = os.path.join(finaldir, 'test' + str(id))
                    historydir = os.path.join(finaldir2, 'history')
                    onlyfiles = [f for f in os.listdir(historydir) if os.path.isfile(os.path.join(historydir, f))]
                    timelinelength = len(onlyfiles)
                    historylist = []
                    for i in range(timelinelength):
                        with open(os.path.join(historydir, onlyfiles[i]), "r") as f:
                            lines = f.readlines()
                        historylist.append(lines)
                    
               
                    codeline = ''.join(historylist[int(value)])

                    
                    return HttpResponse(codeline)
                except FileNotFoundError:
                    codeline = "The coding file could not be found, backend error"
                    return HttpResponse(codeline)
            elif Reviewer.objects.filter(user=User.objects.get(username=username)).exists():
                username = request.session.get('scandidate')
                try:
                    USER_DIR = os.path.join(settings.MEDIA_DIR, 'users')
                    finaldir = os.path.join(USER_DIR, username)
                    testname = "test" + str(id)
                    finaldir2 = os.path.join(finaldir, testname)
                    historydir = os.path.join(finaldir2, 'history')
                    onlyfiles = [f for f in os.listdir(historydir) if os.path.isfile(os.path.join(historydir, f))]
                    timelinelength = len(onlyfiles)
                    historylist = []
                    for i in range(timelinelength):
                        with open(os.path.join(historydir, onlyfiles[i]), "r") as f:
                            lines = f.readlines()
                        historylist.append(lines)
                    
               
                    codeline = ''.join(historylist[int(value)])
                    return HttpResponse(codeline)
                except FileNotFoundError:
                    codeline = "The coding file could not be found, backend error"
                    return HttpResponse(codeline)
    return render(request, 'cs14/codereview.html', {'code':lines, 'language': language , 'taskDec':taskDec, 'taskout':taskout})

