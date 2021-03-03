from django.test import TestCase
from django.test import Client
from django.urls import reverse
from cs14.models import Candidate, Admin, Results, Reviewer, Task, UserTask, Profile

class resultsTest(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(username='testuser')
        test_user.set_password('testpassword')
        test_user.save()
        testTask = Task.objects.get(taskID=1)
        Candidate.objects.create(user=test_user)
        candidate = candidate.objects.get(user=test_user)
        Results.objects.create(userID=candidate, passpercentage =80, taskID=testTask, tests_passed=4, tests_failed=1, timetaken=1, complexity="test", language="java")
        self.response = self.client.get(reverse('cs14:results'))
        self.content = self.response.content.decode()
      
    
    def test_result(self):
        c = Client()
        c.login(username='testuser', password='testpassword')
        self.assertContains(response, '<table class="tg"><thead><tr><th class="tg-0lax">Task ID</th> <th class="tg-0lax"> Tests Passed</th><th class="tg-0lax">Tests Failed</th><th class="tg-0lax">Pass Percentage</th><th class="tg-0lax">Time taken</th><th class="tg-0lax"> Complexity </th><th class="tg-0lax">Description</th><th class="tg-0lax">Code</th></tr> </thead><tbody><tr><td class="tg-0lax">1</td><td class="tg-0lax">4</td> <td class="tg-0lax">1</td><td class="tg-0lax">80</td><td class="tg-0lax">1</td><td class="tg-0lax">test</td></tr></tbody></table>', status_code=200)
    