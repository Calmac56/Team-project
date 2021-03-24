from django.test import TestCase
from django.test import Client
from django.urls import reverse
from cs14.models import Candidate, Admin, Results, Reviewer, Task, UserTask, Profile
from django.contrib.auth.models import User
import shutil
import os
from django.conf import settings
import time


class resultsTest(TestCase):   #Results page testing class
    @classmethod
    def setUpTestData(self):
     
        test_user = User.objects.create_user(username='testuser')
        test_user.set_password('testpassword')
        test_user.save()
        document.getElementById('inputArea') test_user2 = User.objects.create_user(username='testuser2')
        test_user2.set_password('testpassword')
        test_user2.save()
        test_admin = User.objects.create_user(username='testAdmin')
        test_admin.set_password('testpassword')
        test_admin.save()
        test_reviewer = User.objects.create_user(username='testReviewer')
        test_reviewer.set_password('testpassword')
        test_reviewer.save()
        rev = Reviewer.objects.create(user=test_reviewer)
        rev.save()
        Admin.objects.create(user=test_admin)
        theadmin = Admin.objects.get(user=test_admin)
        Task.objects.create(taskID=1, description="testTask", testcases="0123", expectedout="0123",creator=theadmin, time=1000)
        Task.objects.create(taskID=2, description="testTask2", testcases="1234", expectedout="1234",creator=theadmin, time=1000)
        testTask = Task.objects.get(taskID=1)
        testTask2 = Task.objects.get(taskID=2)
        Candidate.objects.create(user=test_user)
        candidate = Candidate.objects.get(user=test_user)
        cand = Candidate.objects.create(user=test_user2)
        candidate2 = Candidate.objects.get(user=test_user2)
        Results.objects.create(userID=candidate, passpercentage =80, taskID=testTask, tests_passed=4, tests_failed=1, timetaken=1, complexity="test", language="java")
        Results.objects.create(userID=candidate2, passpercentage=80,taskID=testTask, tests_passed=4, tests_failed=1, timetaken=1, complexity="test", language="java")
        Results.objects.create(userID=candidate2, passpercentage=60,taskID=testTask2, tests_passed=3, tests_failed=2, timetaken=1, complexity="test", language="java")
        
    def test_candidate_result(self):  #Tests if correct result shows up for out test candidate
        c = Client()
        user= c.login(username='testuser', password='testpassword')
        candidate = Candidate.objects.get(user=user)
        response = c.get(reverse('cs14:cresults'))
      
        self.assertEquals(list(response.context['results'].values_list()), list(Results.objects.filter(userID=candidate).values_list()))
        print("Candidate result ok")
    
    def test_reviewer_result(self):  #Tests if correct result shows up for out test candidate to our reviewer

        c = Client()
        user = c.login(username='testReviewer', password='testpassword')
        candidate = Candidate.objects.get(user=User.objects.get(username='testuser'))
        response = c.get('/cs14/results/', {'state':'testuser'})
        self.assertEquals(list(response.context['results'].values_list()), list(Results.objects.filter(userID=candidate).values_list()))
        print("Reviewer results ok")
    
    def test_candidate_numresult(self):  #Tests if correct number of results shows up to our test candidate
        c = Client()
        user= c.login(username='testuser2', password='testpassword')
        candidate = Candidate.objects.get(user=user)
        response = c.get(reverse('cs14:cresults'))
        self.assertEqual(len(response.context['results']), 2)
        print("Number of candidate results ok")
       
    def test_reviewer_numresult(self):    #Tests if correct number of results shows four our test candidate to reviewers
        c = Client()
        user = c.login(username='testReviewer', password='testpassword')
        candidate = Candidate.objects.get(user=User.objects.get(username='testuser'))
        response = c.get('/cs14/results/', {'state':'testuser2'})
        self.assertEquals(len(response.context['results']), 2)
        print("Number of reviewer results ok")
 

class reviewTest(TestCase):

    @classmethod
    def setUpTestData(self):
        test_user = User.objects.create_user(username='testuser')
        test_user.set_password('testpassword')
        test_user.save()
        test_admin = User.objects.create_user(username='testAdmin')
        test_user.set_password('testpassword')
        test_user.save()
        Admin.objects.create(user=test_admin)
        theadmin = Admin.objects.get(user=test_admin)
        Task.objects.create(taskID=1, description="testTask", testcases="0123", expectedout="0123",creator=theadmin, time=1000)
        testTask = Task.objects.get(taskID=1)
        Candidate.objects.create(user=test_user)
        candidate = Candidate.objects.get(user=test_user)
        Results.objects.create(userID=candidate, passpercentage =80, taskID=testTask, tests_passed=4, tests_failed=1, timetaken=1, complexity="test", language="java")
            
        self.c = Client()
        self.user= self.c.login(username='testuser', password='testpassword')
        self.c.post('/cs14/sendCode', {'language':'python', 'codeArea':'print("Hello world")'})
      
  
        
    def test_run(self):   #Tests if we can run code on our code review page and that it gives correct output
      
        response = self.c.get(reverse('cs14:creview', kwargs={'id':1}))
        theresp = self.c.post('/cs14/testCode',{'language':'python', 'codeArea':response.context["code"]})
        theresp = theresp.content.decode('ascii')
        contains = 'Test Case 1:' in theresp
    
        self.assertTrue(contains)
        print("Code execution on review page ok")
    
    def test_inital_page(self):  #Tests if the inital code review page shows the correct code for test candidate
        
        self.c.post('/cs14/sendCode', {'language':'python', 'codeArea':'print("Hello world from calum")'})
        
        response = self.c.get(reverse('cs14:creview', kwargs={'id':1}))
        code = response.context["code"]
        self.assertEqual(['print("Hello world from calum")'], code)
        print("Intial review page ok")

    def test_custom_input(self):  #Tests if custom input for executing code works on review page
        response = self.c.get(reverse('cs14:creview', kwargs={'id':1}))
        theresp = self.c.post('/cs14/testCode',{'language':'python', 'codeArea':response.context["code"], 'inputArea':123, 'customInputCB':'true'})
        theresp = theresp.content.decode('ascii')
        contains = 'Custom output:' in theresp
        self.assertTrue(contains)
        print("Custom input works ok")

   
    @classmethod
    def tearDownClass(self): #Cleans up backend testing files
        USER_DIR = os.path.join(settings.MEDIA_DIR, 'users')
        shutil.rmtree(os.path.join(USER_DIR, 'testuser'))
    



        
