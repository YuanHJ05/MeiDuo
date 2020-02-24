from django.urls import path, re_path
from . import views

app_name = 'verifycation'
urlpatterns = [
    re_path('image_codes/(?P<uuid>[\w-]+)/$', views.ImageCodeView.as_view(), name='imagecode'),
]
