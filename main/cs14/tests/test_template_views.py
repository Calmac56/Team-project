from django.test import TestCase
from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User
from cs14.models import Candidate
from cs14.views import *

# Test cases to check the templates are loading correctly
class templateTests(TestCase):

    @classmethod
    def setUpTestData(self):
        self.c = Client()
        
    def test_python_template(self):
        resp = self.c.post('/cs14/updateTemplate', {'language':'python'}).content.decode('ascii')
        worked = "input_data = [int(x.strip()) for x in sys.argv[1].split('\\n')]" in resp
        self.assertTrue(worked)

    def test_java_template(self):
        resp = self.c.post('/cs14/updateTemplate', {'language':'java'}).content.decode('ascii')
        worked = "public static void main(String[] args) {" in resp
        self.assertTrue(worked)