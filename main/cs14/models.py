from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from datetime import datetime, timezone

# Create your models here.
class Admin (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username

class Candidate (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username

class Reviewer (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username

class Task(models.Model):
    taskID = models.IntegerField(primary_key=True)
    description = models.CharField(max_length = 4095)
    testcases = models.CharField(max_length = 255)
    expectedout = models.CharField(max_length = 255)
    creator = models.ForeignKey(Admin, on_delete=models.CASCADE)
    time = models.IntegerField(default=300) #time in seconds

class UserTask (models.Model):
    userID =  models.ForeignKey(Candidate, on_delete=models.CASCADE)
    taskID = models.ForeignKey(Task, on_delete=models.CASCADE)

class Results(models.Model):
    userID =  models.ForeignKey(Candidate, on_delete=models.CASCADE)
    taskID = models.ForeignKey(Task, on_delete=models.CASCADE)
    tests_passed = models.IntegerField()
    tests_failed = models.IntegerField()
    passpercentage = models.IntegerField() #have made this int, but should be calculated
    timestarted = models.DateTimeField(default=datetime.now)
    timetaken = models.IntegerField()
    complexity = models.CharField(max_length = 31)
    language = models.CharField(max_length = 255)
    completed = models.BooleanField(default=False)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(default = "profile1.png", upload_to='static/images/', blank =True)
    
    def __str__(self):
        return self.user.username

def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = Profile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender=User)