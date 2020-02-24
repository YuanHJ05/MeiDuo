from django.urls import path, re_path
from . import views

app_name = 'users'
urlpatterns = [
    path('register.html', views.RegisterView.as_view(), name='register'),
    re_path('usernames/(?P<username>[a-zA-Z0-9_-]{5,20})/count/$', views.UsernameCountView.as_view(),
            name='usernamecount'),  # 验证用户名是否重复
    re_path('mobiles/(?P<mobile>1[345789]\d{9})/count/$', views.MobileCountView.as_view(), name='mobilecount')
]
