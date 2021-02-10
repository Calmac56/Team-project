from django.contrib import admin
from cs14.models import Candidate, Admin, Task, Results, Reviewer, UserTask

# Register your models here.

themodels = [Candidate, Admin, Task, Results, Reviewer, UserTask]
admin.site.register(themodels)
