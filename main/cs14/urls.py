from django.urls import path
from cs14 import views

app_name = 'cs14'

urlpatterns = [
	path('', views.index, name='index'),
	path('code', views.codingPage, name='code'),
	path('sendCode', views.sendCode, name='sendCode'),
	path('register/', views.register, name='register'),
	path('login/', views.loginPage, name='login'),
	path('logout/', views.logoutUser, name='logout'),
	path('results/', views.results, name='results'),
	path('myresults/', views.cresults, name='cresults'),
	path('codereview/<int:id>/', views.creview, name='creview'),
	path('testCode', views.testCode, name='testCode'),
<<<<<<< HEAD
	path('rhistory', views.rhistory, name='rhistory'),
=======
>>>>>>> 6c09f6baa324d4867bf10c33998b797806ba0dfc
]
