from django.test import TestCase
from static.python.compile import *

class LanguageExtensionTest(TestCase):
    filename = "test"
    def test_java(self):
        language = "java"
        self.assertEquals(add_language_extension(self.filename, language), "test.java", "Java extension failed.")
        print("Java extension OK")

    def test_python(self):
        language = "python"
        self.assertEquals(add_language_extension(self.filename, language), "test.py", "Python extension failed.")
        print("Python extension OK")

    def test_unknown_language(self):
        language = "gibberish"
        self.assertRaises(Exception, add_language_extension, self.filename, language), "FAILED: exception for unknown language not raised."
        print("Exception raised for unknown language OK.")
