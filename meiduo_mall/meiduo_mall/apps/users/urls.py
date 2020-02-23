from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path('register.html', views.RegisterView.as_view(), name='register'),
]
