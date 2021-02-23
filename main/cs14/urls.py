from django.urls import path
from cs14 import views
from django.conf.urls.static import static
from django.conf import settings


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
	path('profile/', views.userprofile, name='profile'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)