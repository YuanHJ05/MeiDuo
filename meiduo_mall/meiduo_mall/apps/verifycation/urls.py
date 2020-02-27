from django.urls import path, re_path
from . import views

app_name = 'verifycation'
urlpatterns = [
    re_path('image_codes/(?P<uuid>[\w-]+)/$', views.ImageCodeView.as_view(), name='imagecode'),
    re_path('sms_codes/(?P<mobile>1[3-9]\d{9})/$', views.SmsCodeView.as_view(), name='smscode')
]
