from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from cs14.forms import CreateUserForm

def index(request):
    return render(request, 'cs14/index.html')

def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
        
    context = {'form': form}
    return render(request, 'cs14/register.html', context)
