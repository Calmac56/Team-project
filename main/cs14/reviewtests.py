from django.test import TestCase
from django.test import Client
from django.urls import reverse
from cs14.models import Candidate, Admin, Results, Reviewer, Task, UserTask, Profile
from django.contrib.auth.models import User
import shutil
import os
from django.conf import settings


class resultsTest(TestCase):
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
    def test_candidate_result(self):
       
        
    
        candidate = Candidate.objects.get(user=self.user)
        response = self.c.get(reverse('cs14:cresults'))
        testuser = response.wsgi_request.user
      
        self.assertEquals(list(response.context['results'].values_list()), list(Results.objects.filter(userID=candidate).values_list()))

 

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
        self.c.post('/cs14/sendCode', {'language':'python', 'codeArea':'print("Hello world from calum")'})
  
        
      
    
    def test_inital_page(self):
        
        
        response = self.c.get(reverse('cs14:creview', kwargs={'id':1}))
        code = response.context["code"]
        self.assertEqual(['print("Hello world from calum")'], code)

    def test_run(self):
      
        response = self.c.get(reverse('cs14:creview', kwargs={'id':1}))
        theresp = self.c.post('/cs14/testCode',{'language':'python', 'codeArea':response.context["code"]})
        theresp = theresp.content.decode('ascii')
        contains = 'Test Case 1:' in theresp
    
        self.assertTrue(contains)

    def test_timeline(self):
        response = self.c.get(reverse('cs14:creview', kwargs={'id':1}))
        theresp = self.c.post('/cs14/rhistory', {'number':0, 'taskID': 1})
        theresp = theresp.content.decode('ascii')
        self.assertEqual('print("Hello world")', theresp)

    @classmethod
    def tearDownClass(self):
        USER_DIR = os.path.join(settings.MEDIA_DIR, 'users')
        shutil.rmtree(os.path.join(USER_DIR, 'testuser'))
    



        
