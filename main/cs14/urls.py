from django.urls import path
from cs14 import views

app_name = 'cs14'

urlpatterns = [
	path('', views.index, name='index'),
]
