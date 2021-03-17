from django.test import TestCase 
from django.contrib.auth.models import User
from cs14.models import Admin, Candidate, Reviewer, Task, UserTask, Results, Profile

class ModelTests(TestCase):
    email = 'email@email.com'
    password = 'testPassword123'

    def test_user(self):
        user = User.objects.create_user('testUser', self.email, self.password)
        self.assertEquals([user.username, user.email], ['testUser',self.email], "User not created properly.")
        print("User created OK")
        return user

    def test_candidate(self):
        user = User.objects.create_user('testCandidate', self.email, self.password)
        candidate, success = Candidate.objects.get_or_create(user=user)
        self.assertEquals([candidate.user.username, candidate.user.email], ['testCandidate', self.email], "Candidate not created properly.")
        print("Candidate created OK")
        return candidate

    def test_reviewer(self):
        user = User.objects.create_user('testReviewer', self.email, self.password)
        reviewer, success = Reviewer.objects.get_or_create(user=user)
        self.assertEquals([reviewer.user.username, reviewer.user.email], ['testReviewer', self.email], "Reviewer not created properly.")
        print("Reviewer created OK")

    def test_admin(self):
        user = User.objects.create_user('testAdmin', self.email, self.password)
        admin, success = Admin.objects.get_or_create(user = user)
        self.assertEquals([admin.user.username, admin.user.email], ['testAdmin', self.email], "Admin not created properly.")
        print("Admin created OK")

    def test_task(self):
        user = User.objects.create_user('testAdmin', self.email, self.password)
        creator, success = Admin.objects.get_or_create(user = user)
        task, success = Task.objects.get_or_create(taskID = 1, description = 'This is a test task', testcases = 'Testcases', expectedout = 'Expectedout', creator=creator)
        self.assertEquals([task.taskID], [1], "Task not created properly.")
        print("Task created OK")
        return task

    def test_userTask(self):
        user = self.test_candidate()
        task = self.test_task()
        userTask, success = UserTask.objects.get_or_create(userID = user, taskID = task)
        self.assertEquals([userTask.userID.user.username, userTask.taskID.taskID], ['testCandidate', 1], 'UserTask not created properly.')
        print("UserTask created OK")

    def test_results(self):
        userID = self.test_candidate()
        taskID = self.test_task()
        result, success = Results.objects.get_or_create(userID = userID, taskID = taskID, tests_passed = 1, tests_failed = 0, passpercentage = 100, timetaken = 10, complexity = 'complexity', language='language')
        self.assertIsInstance(result, Results, "Result not created properly")
        print("Result created OK")
    
    def test_profile(self):
        user = self.test_user()
        profile, success = Profile.objects.get_or_create(user = user)
        self.assertIsInstance(profile, Profile, "Profile not created properly")
        print("Profile created OK")