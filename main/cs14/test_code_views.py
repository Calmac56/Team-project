from django.test import TestCase
from django.test import Client
from django.urls import reverse


from django.contrib.auth.models import User
from cs14.models import Candidate
from cs14.views import *
# Create your tests here.
class test_views(TestCase):
    def setUp(self):
        
        self.u = User.objects.create(username='testuser')
        self.u.set_password('password')
        self.u.save()
        self.u = Candidate.objects.create(user=self.u)
        self.u.save()
        self.c = Client()
        
    
    def test_code_send(self):
        login = self.c.login(username='testuser', password='password')
        resp = self.c.post('/cs14/sendCode', {'language':'python', 'codeArea':'print("Hello World")', 'taskID':'1'})
        response = resp.content.decode('ascii')
        contains = 'Test Case 1:' in response
        self.assertTrue(contains)


    #add nice response here
    # def test_send_code_guest_user(self):
    #     resp = self.c.post('/cs14/sendCode', {'language':'python', 'codeArea':'print("Hello World")'})
    #     response = resp.content.decode('ascii')
    #     contains = 'unauthenticated' in response
    #     self.assertTrue(contains)

    def test_code_send_syntax_error(self):
        login = self.c.login(username='testuser', password='password')
        resp = self.c.post('/cs14/sendCode', {'language':'python', 'codeArea':'print("Hello World"', 'taskID':'1'})
        response = resp.content.decode('ascii')
        contains = 'SyntaxError' in response
        self.assertTrue(contains)

    def test_custom_input(self):
        login = self.c.login(username='testuser', password='password')
        code = '''import sys\nfor elt in sys.argv:\n\tprint(elt)'''
        resp = self.c.post('/cs14/sendCode', {'language':'python', 'codeArea':code, 'customInputCB':'true', 'inputArea':'1\n2\n3', 'taskID':'1'})
        response = resp.content.decode('ascii')
        contains = '1\n2\n3' in response and 'Custom output:' in response
        print(response)
        self.assertTrue(contains)


    # returning 301 ???
    # def test_login(self):
    #     login = self.c.login(username='testuser', password='password')
    #     resp = self.c.post('/cs14/login')
    #     print('-'*30,resp) 

        


# class exampleTestCase(TestCase):
#     def setUp(self):
#         SETUP CODE GOES HERE
    
#     def test_example(self):
#         TEST CODE GOES HERE
#         self.assertEqual(1, 1)
