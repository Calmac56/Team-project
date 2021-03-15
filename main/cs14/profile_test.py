from django.test import TestCase
from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User

class test_ProfilePage(TestCase):

    def setUpTestData(cls):
        user.objects.create(first_name='Harry', last_name='Potter', email ="Testing@gmail.com")

    def test_first_name_label(self):
        user = user.objects.get(id=1)
        field_label = user._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label,'first name')
        print("First name label OK")
    
    def test_last_name_label(self):
        user = user.objects.get(id=1)
        field_label = user._meta.get_field('last_name').verbose_name
        self.assertEqual(field_label,'last name')
        print("Last name label OK")

    def test_email(self):
        user = user.objects.get(id=1)
        field_label = user._meta.get_field('last_name').verbose_name
        self.assertEqual(field_label,'last name')
        print("Email OK")

    def test_object_name_is_last_name_comma_first_name(self):
        user = user.objects.get(id=1)
        expected_object_name = f'{user.last_name}, {user.first_name}'
        self.assertEqual(expected_object_name, str(user))
        print("Name is last name comma first name")

    def test_ProfilePage_url(self):
        self.assertTemplateUsed(self.response, 'cs14/profile.html')
        print("Profile page access success")
    
