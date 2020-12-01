from django.contrib import admin
from cs14.models import Candidate, Admin, Task, Results, Reviewer

# Register your models here.

themodels = [Candidate, Admin, Task, Results, Reviewer]
admin.site.register(themodels)
