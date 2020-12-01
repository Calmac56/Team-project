from django.contrib import admin
from cs14.models import Candidate, Admin, Task, Results

# Register your models here.

themodels = [Candidate, Admin, Task, Results]
admin.site.register(themodels)
