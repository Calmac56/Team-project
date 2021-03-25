from django.shortcuts import render, redirect
from django.http import HttpResponse
from static.python.compile import * #compilation functions
from static.python.getuserdir import *
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm, CreateLoginLink, Profile
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from sesame.utils import get_query_string
from django.core.mail import send_mail
from cs14.models import Candidate, Admin, Results, Reviewer, Task, UserTask, Profile
import json
import datetime
import os
import shutil



def index(request):
    return render(request, 'cs14/index.html')

def getCookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        return default_val

    return val

@login_required
def codingPage(request, id):
    context = {}
    result = None

    try:
        task = Task.objects.filter(taskID=id)
        if len(task) == 0:
            raise Task.DoesNotExist
        else:
            task = Task.objects.filter(taskID=id)[0]
        taskDec = task.description
        taskout = task.expectedout
        
        userObj = User.objects.get(username=request.user)
        candidate = Candidate.objects.get(user=userObj)

        if Results.objects.filter(userID=candidate, taskID=task).exists():
           
            if Results.objects.filter(userID=candidate, taskID=task)[0].completed:
                return redirect('cs14:profile')
        else:
            Results.objects.create(userID=candidate, passpercentage =0, taskID=task, tests_passed=0, tests_failed=0, timetaken=1, complexity="test", language="test")
        
        result = Results.objects.filter(userID=candidate, taskID=task)[0]

    except Task.DoesNotExist:
        return redirect('cs14:profile')

    context['language'] = getCookie(request, 'language', default_val='java')
    context['code'] = getCookie(request, 'code', default_val='')
    context['input'] = getCookie(request, 'input', default_val='')
    context['taskDec'] = taskDec
    context['taskout'] = taskout
    
    #code to deal with auto templating code for users
    context['taskID'] = id
    if context['code'] == '':
        TEMPLATE_PATH = os.path.join(settings.MEDIA_DIR, 'templates', context['language']+'.txt')
        with open(TEMPLATE_PATH, 'r') as f:
            template_code = f.read()
        context['code'] = template_code
        
    #code to initialize timer
    time_now = datetime.datetime.now(datetime.timezone.utc)
    time_started = result.timestarted.replace(tzinfo=datetime.timezone.utc)
    time_since_started = int((time_now - time_started).total_seconds())
    context['time'] = task.time - time_since_started
    context['time_total'] = task.time
    print(task.time - time_since_started)

    if task.time - time_since_started < 0:
        context['submit'] = 'true'
    else:
        context['submit'] = 'false'


    return render(request, 'cs14/codingPage.html', context=context)

def codingPageCookie(request):
    request.session['language'] = request.POST.get('language').lower()
    request.session['code'] = request.POST.get('code')
    request.session['input'] = request.POST.get('input')

    return HttpResponse('saved')

    
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
        
            filename = 'main'
            testname = 'test' + str(request.POST.get('taskID'))

            if language == 'python':
                filename += '.py'
            elif language == 'java':
                filename+= '.java'
            

            filepath = os.path.join(USER_DIR, username, testname)

            try:
                os.makedirs(os.path.join(filepath, 'history'))
            except FileExistsError:
                pass
            with open(os.path.join(filepath, filename), 'w+') as f:
                f.write(request.POST.get('codeArea').strip().replace(chr(160), " "))
            with open(os.path.join(filepath, 'history',str(datetime.datetime.now()) + '.txt'), 'w+') as f:
                f.write(request.POST.get('codeArea').strip().replace(chr(160), " "))

            #Custom input functionality
            customInputCB = request.POST.get('customInputCB')
            if customInputCB == 'true':
                customInputText = request.POST.get('inputArea')
           

                try:
                    tempInputFile = os.path.join(USER_DIR, username, 'tempInput.txt')
                    with open(tempInputFile, 'w') as f:
                        f.write(customInputText)
                    #run the test from compile.py
                    results_output = test(candidate, testname, username, language, tempInputFile)
                except FileExistsError:
                    pass
            else:
                results_output, passes, fails = test(candidate, testname, username, language)
            

        else:
            return None
    
        return_text = ""
       
        
        #Store test results in DB
        if customInputCB == 'true':
            return_text = "Custom output: \n" + results_output[1].decode('utf-8')

        else:
            #Let user know they can't submit with custom input
            print("Tests passed: ", passes)
            print("Tests failed: ", fails)

            if submission == 'true':

                
                del request.session['language']
                del request.session['code']
                # ----------------------READ----------------------------------------------
                # still need to properly add complexity, time taken (timer), code
                # current values are for test purposes
                testTask = Task.objects.get(taskID=int(request.POST.get('taskID')))

                # reset session variables
                request.session['language'] = ""
                request.session['code'] = ""
                request.session['input'] = ""

                # remove container
                containerID = getattr(candidate, "containerID")
                if len(containerID) != 0:
                    remove_container(containerID)
                
                # set candidate's assigned container to blank
                Candidate.objects.filter(user=candidate.user).update(containerID='')

                # ----------------------READ----------------------------------------------
                # still need to properly add complexity, time taken (timer), code
                # current values are for test purposes
                
                testTask = Task.objects.get(taskID=int(request.POST.get('taskID')))
                result = Results.objects.filter(userID=candidate, taskID=testTask)[0]


                time_now = datetime.datetime.now(datetime.timezone.utc)
                time_started = result.timestarted.replace(tzinfo=datetime.timezone.utc)
                time_taken = int((time_now - time_started).total_seconds())
                
                Results.objects.filter(userID=candidate, taskID=testTask).update(passpercentage = int(passes/(passes+fails)*100), tests_passed=passes, tests_failed=fails, timetaken=time_taken, complexity="test", language=language, completed=True)


            for result in results_output:
                if type(result) == type(True):
                    return_text+= str(result)
                elif type(result) == type("abc"):
                    return_text+= str(result)
                else:
                    return_text+= str(result.decode("ASCII"))
            return_text += "Tests passed: " + str(passes) + "\n" + "Tests failed: " + str(fails) + "\n"
  
    return HttpResponse(return_text)

"""  
This is a function to test code on the review page. Returns test output back to the page.

Everything is writen to temporary files to execute then deleted as we dont want reviewers or users to modify submitted code permanently. 
"""
    

def testCode(request):  
    results = []
    if(request.method == 'POST'):
        if request.user.is_authenticated:
            foldername = str(request.user.username)
            USER_DIR = os.path.join(settings.MEDIA_DIR, 'users')
            if Reviewer.objects.filter(user=request.user):
                username = request.session['scandidate']
                
            else:
                
                username = request.user.username
            language = request.POST.get('language').lower()

            
            
            
            filename = 'main'
            testname = 'test' + str(request.POST.get('taskID'))
            if language == 'python':
                filename += '.py'
            elif language == 'java':
                filename+= '.java'
            
            filepath = os.path.join(USER_DIR, username, testname)
            try:
                os.makedirs(os.path.join(filepath, foldername, 'temp'))
            except FileExistsError:
                pass
            with open(os.path.join(filepath, foldername, 'temp', filename), 'w+') as f:
                f.write(request.POST.get('codeArea').strip().replace(chr(160), " "))
            
            customInputCB = request.POST.get('customInputCB')
            if customInputCB != 'true':
                
                results,passes,fails = reviewtest(testname, username, language,foldername)
            
            if customInputCB == 'true':
                customInputText = request.POST.get('inputArea')
                try:
                    tempInputFile = os.path.join(USER_DIR, username, 'tempInput.txt')
                    with open(tempInputFile, 'w') as f:
                        f.write(customInputText)
                    #run the test from compile.py
                    results = reviewtest(testname, username, language, foldername, tempInputFile)
                except FileExistsError:
                    pass
           
            
        else:
            return None
        return_text = ""

        try:
            shutil.rmtree(os.path.join(USER_DIR, username, testname,foldername, 'temp'))
        except FileNotFoundError:
            pass
        
        if customInputCB == 'true':
            return_text = "Custom output: \n" + results[1].decode('utf-8')
        
        else:
      
            for result in results:
                if type(result) == type(True):
                    return_text+= str(result)
                elif type(result) == type("abc"):
                    return_text+= str(result)
                else:
                    return_text+= str(result.decode("ASCII"))
            
            return_text += "Tests passed: " + str(passes) + "\n" + "Tests failed: " + str(fails) + "\n"
    
    else:
        return redirect("cs14:index")
    
    return HttpResponse(return_text)


""" 
This is a view that renders the generate user page. Checks if the user is an Admin and allows them to fill in a form to create an account.
Then uses the gmail api to send the new user an email with their accoutn detail. Including a 2 week sign in link and a randomly generated password.

"""

@login_required
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

                message = "User account created for " + str(username)

                messages.add_message(request, messages.SUCCESS, message)
                
                return redirect('cs14:register')
            
            else:
                 messages.add_message(request, messages.ERROR, 'Account already generated for this email')

    else:
        return redirect('cs14:login')

        
    context = {'form': form}
    return render(request, 'cs14/register.html', context)


""" 
This is a view to render the login page. Renders a simple login form and allows the user to login.
Returns an error meesage to the page if an incorrect username or password is used. 
"""
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
                messages.error(request, 'Username or password is incorrect')

    context = {}
    return render(request, 'cs14/login.html')

def logoutUser(request):
    logout(request)
    return redirect('cs14:login')


""" 
Stores a session variable for use on the results page dropdown menu
"""

def getresultsession(request):
    if not request.is_ajax():
        return redirect('cs14:index')

    return HttpResponse(request.session['scandidate'])

@login_required
def results(request):

    result = None
    searchcompleted = False
    allcandiates = Candidate.objects.all()

    try:
        if request.user.is_authenticated:
            auser = Reviewer.objects.get(user=request.user)
        else:
            auser = None
    except Reviewer.DoesNotExist:
        auser = None

    if auser == None:
        return redirect('cs14:login')
    

   
    if request.session.get('scandidate'):
        theuser =  User.objects.get(username = request.session.get('scandidate'))
        candidate = Candidate.objects.get(user = theuser)
        result = Results.objects.filter(userID = candidate)
        
        if not result:
            result = None
    
    
    

    if 'state' in request.GET:
        searched  = request.GET['state']
        
        
        try:
            theuser =  User.objects.get(username = searched)
            try:
                candidate = Candidate.objects.get(user = theuser)
                request.session['scandidate'] = request.GET['state']
                result = Results.objects.filter(userID = candidate)
                if not result:
                    result = None

            
            except Candidate.DoesNotExist:
                result = None
           
        except User.DoesNotExist:
            result = None



    return render(request, 'cs14/results.html', {'results':result, 'searched':searchcompleted, 'candidates':allcandiates})

""" 
View that returns the results that a candidate got back to them. These results are read from the database.

"""
@login_required
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


""" 
View that renders the code review page. Takes in the task id from the URL. Reads code from backend files.
Creates timeline length by getting amount of history files.
"""
@login_required
def creview(request,id):


    try:
        task = Task.objects.filter(taskID=id)
        taskDec = task[0].description
        taskout = task[0].expectedout
    except:
        taskDec = "Could not get task description"
        taskout = "Could not get expected output"


    
    if request.user.is_authenticated:
        lines = []
        username = request.user.get_username()
        if Candidate.objects.filter(user=User.objects.get(username=username)).exists():
            theresult = Results.objects.filter(userID=Candidate.objects.filter(user=User.objects.get(username=username)).exists(), taskID=id)
            try:
                language = theresult[0].language
            except:
                language = "python"
            
            timelinelength, lines = getlines(id, username)
        elif Reviewer.objects.filter(user=User.objects.get(username=username)).exists():
            username = request.session.get('scandidate')
            theresult = Results.objects.filter(userID=Candidate.objects.filter(user=User.objects.get(username=username)).exists(), taskID=id)
            try:
                language = theresult[0].language
            except:
                language = "python"
            timelinelength, lines = getlines(id, username)

        else:
            return redirect('cs14:home')
    
    else:
        return redirect('cs14:login')

                


    return render(request, 'cs14/codereview.html', {'code':lines, 'language': language , 'taskDec':taskDec, 'taskout':taskout, 'slideval':timelinelength, 'taskID':id})


""" 
View that fetches the required file data for the timeline using post requests. 
"""
@login_required
def rhistory(request):
    lines = []
   
    if(request.method == 'POST'):
        if request.user.is_authenticated:
            username = request.user.get_username()
            value = request.POST.get("number")
            id  = request.POST.get("taskID")
     
            
            if Candidate.objects.filter(user=User.objects.get(username=username)).exists():
                codeline = gethistory(username,id, value)
                
                
                return HttpResponse(codeline)
            elif Reviewer.objects.filter(user=User.objects.get(username=username)).exists():
                username = request.session.get('scandidate')
                codeline = gethistory(username,id, value)

                return HttpResponse(codeline)
    else:
        return redirect('cs14:index')

@login_required
def profile(request):
    name = request.user.get_username  # change this to full name

    tasks = []
    results = []
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
            
            taskobjs = UserTask.objects.filter(userID = candidate)

            try:
                resultsobjs = Results.objects.filter(userID=candidate)
                for result in resultsobjs:
                    if result.completed == True:
                        results.append(result.taskID.taskID)
            except Results.DoesNotExist:
                results = None

            for task in taskobjs:
                tasks.append(task.taskID)

            if not tasks:
                tasks = None

            
        except Candidate.DoesNotExist:
            tasks = None
           
    except User.DoesNotExist:
        tasks = None
    
    if request.method == 'POST':
        form = CreateUserForm(request.POST, request.FILES or None)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
    else:
        form = CreateUserForm()

    return render(request, 'cs14/profile.html', {'name':name, 'tasks':tasks, 'form':form, 'results':results})