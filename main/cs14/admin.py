from django.contrib import admin
from cs14.models import Candidate, Admin, Task, Results, Reviewer, UserTask, Profile

# Register your models here.

themodels = [Candidate, Admin, Task, Results, Reviewer, UserTask, Profile]
admin.site.register(themodels)
