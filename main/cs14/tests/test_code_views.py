from django.test import TestCase
from django.test import Client
from django.urls import reverse


from django.contrib.auth.models import User
from cs14.models import Candidate
from cs14.views import *


# Test cases to ensure the code compilation and correlating views work correctly
class test_views(TestCase):

    @classmethod
    def setUpTestData(self):
        self.u = User.objects.create(username='usertest1')
        self.u.set_password('password')
        self.u.save()
        self.u = Candidate.objects.create(user=self.u)
        self.u.save()
        self.c = Client()
        
    
    def test_code_send(self):
        login = self.c.login(username='usertest1', password='password')
        resp = self.c.post('/cs14/sendCode', {'language':'python', 'codeArea':'print("Hello World")', 'taskID':'1'})
        response = resp.content.decode('ascii')
        contains = 'Test Case 1:' in response
        self.assertTrue(contains)

    def test_code_send_syntax_error(self):
        login = self.c.login(username='usertest1', password='password')
        resp = self.c.post('/cs14/sendCode', {'language':'python', 'codeArea':'print("Hello World"', 'taskID':'1'})
        response = resp.content.decode('ascii')
        contains = 'SyntaxError' in response
        self.assertTrue(contains)

    def test_custom_input(self):
        login = self.c.login(username='usertest1', password='password')
        code = '''import sys\nfor elt in sys.argv:\n\tprint(elt)'''
        resp = self.c.post('/cs14/sendCode', {'language':'python', 'codeArea':code, 'customInputCB':'true', 'inputArea':'1\n2\n3', 'taskID':'1'})
        response = resp.content.decode('ascii')
        contains = '1\n2\n3' in response and 'Custom output:' in response
        print(response)
        self.assertTrue(contains)
