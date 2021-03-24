from django.test import TestCase
from django.test import Client
from django.urls import reverse
# Create your tests here.
class test_template_used(TestCase):
    def setUp(self):
        self.response = self.client.get(reverse('cs14:index'))
        self.content = self.response.content.decode()
    def test_example(self):
        self.assertTemplateUsed(self.response, 'cs14/index.html')

# class exampleTestCase(TestCase):
#     def setUp(self):
#         SETUP CODE GOES HERE
    
#     def test_example(self):
#         TEST CODE GOES HERE
#         self.assertEqual(1, 1)