from django.db import models

# Create your models here.

class Candidate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length = 255) 
    last_name = models.CharField(max_length = 255)
    userID = models.IntegerField(primary_key=True)
    admin = False
    #email and password in user model?

    def __str__(self):
        return self.user.username


class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length = 255) 
    last_name = models.CharField(max_length = 255)
    userID = models.IntegerField(primary_key=True)
    admin = True
    #email and password in user model?

    def __str__(self):
        return self.user.username

class Task(models.Model):
    taskID = models.IntegerField(primary_key=True)
    description = models.CharField(max_length = 4095)
    testcases = models.CharField(max_length = 255)
    expectedout = models.CharField(max_length = 255)
    creator = models.ForeignKey(Admin, on_delete=models.CASCADE)

class Results(models.Model):
    userID =  models.ForeignKey(Candidate, on_delete=models.CASCADE)
    taskID = models.ForeignKey(Task, on_delete=models.CASCADE)
    tests_passed = models.IntegerField()
    tests_failed = models.IntegerField()
    passpercentage = models.IntegerField() #have made this int, but should be calculated
    timetaken = models.IntegerField()
    complexity = models.CharField(max_length = 31)
    code = models.CharField(max_length = 255)
