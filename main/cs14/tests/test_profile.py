from django.test import TestCase
from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User
from cs14.models import *
from django.core.files.uploadedfile import SimpleUploadedFile

class test_ProfilePage(TestCase):
    #email = "Testing@gmail.com"
    #first_name='Harry'
    #last_name='Potter'

    def test_first_name_label(self):
        user = User.objects.create(first_name='Harry', last_name='Potter', email = "Testing@gmail.com")  
        field_label = user._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label,'first name')
        print("Last name label OK")
    
    def test_last_name_label(self):
        user = User.objects.create(first_name='Harry', last_name='Potter', email = "Testing@gmail.com")  
        field_label = user._meta.get_field('last_name').verbose_name
        self.assertEqual(field_label,'last name')
        print("Last name label OK")

    def test_email(self):
        user = User.objects.create(first_name='Harry', last_name='Potter', email = "Testing@gmail.com")  
        field_label = user._meta.get_field('email').verbose_name
        self.assertEqual(field_label,'email address')
        print("Email OK")
    
    
