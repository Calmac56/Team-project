from django.urls import path
from cs14 import views

app_name = 'cs14'

urlpatterns = [
	path('', views.index, name='index'),
	path('register/', views.register, name='register'),
	path('login/', views.loginPage, name='login')
]
