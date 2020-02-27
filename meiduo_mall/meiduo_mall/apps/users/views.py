from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden, JsonResponse
from django.contrib.auth import login
from django.views import View
from .models import User
from meiduo_mall.utils.response_code import *
from django_redis import get_redis_connection
import re


# Create your views here.
class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        # 接收
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        password2 = request.POST.get('cpwd')
        mobile = request.POST.get('phone')
        sms_code = request.POST.get('msg_code')
        allow = request.POST.get('allow')

        # 验证
        # 1.数据非空
        if not all([username, password, password2, mobile, sms_code, allow]):
            return HttpResponseForbidden('填写数据不完整')
        # 验证用户名
        if not re.match('^[a-zA-Z0-9_-]{5,20}$', username):
            return HttpResponseForbidden('用户名为5-20个字符')
        # 用户名不能重复
        if User.objects.filter(username=username).count() > 0:
            return HttpResponseForbidden('用户名已经存在')
        # 密码
        if not re.match('^[0-9A-Za-z]{8,20}$', password):
            return HttpResponseForbidden('密码为8-20个字符')
        # 确认密码
        if password != password2:
            return HttpResponseForbidden('两次密码不一致！')
        # 手机号码验证
        if not re.match('^1[3456789]\d{9}$', mobile):
            return HttpResponseForbidden('手机号码格式不正确！')
        # 手机号不能重复
        if User.objects.filter(mobile=mobile).count() > 0:
            return HttpResponseForbidden('手机号码不能重复！')
        # 手机短信验证码
        # 读取redis中的短信验证码
        redis_cli = get_redis_connection('sms_code')
        sms_code_redis = redis_cli.get(mobile)  # bytes类型
        if sms_code_redis is None:
            return HttpResponseForbidden('短信验证码已经过期')
        redis_cli.delete(mobile)  # 从redis中删除短信验证码
        redis_cli.delete(mobile + '_flag')
        if sms_code_redis.decode() != sms_code:  # 要先转换为字符类型
            return HttpResponseForbidden('短信验证码错误！')
        # 处理
        # 1.创建用户对象
        user = User.objects.create(
            username=username,
            password=password,
            mobile=mobile
        )
        # 存入数据库
        user.save()
        # 2.状态保持(存入session)
        login(request, user)

        # 响应
        return redirect('/')


# 验证用户名是否重复
class UsernameCountView(View):
    def get(self, request, username):
        username_count = User.objects.filter(username=username).count()
        # 返回json数据
        return JsonResponse({'count': username_count, 'code': RETCODE.OK, 'errmsg': 'OK'})


# 验证手机号码是否重复
class MobileCountView(View):
    def get(self, request, mobile):
        mobile_count = User.objects.filter(mobile=mobile).count()
        return JsonResponse({'count': mobile_count, 'code': RETCODE.OK, 'errmsg': 'OK'})
