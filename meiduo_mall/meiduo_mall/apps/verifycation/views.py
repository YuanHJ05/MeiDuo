from django.shortcuts import render
from django.views import View
from meiduo_mall.libs.captcha.captcha import captcha
from django_redis import get_redis_connection
from . import constans
from django.http import HttpResponse


# Create your views here.
class ImageCodeView(View):
    def get(self, request, uuid):
        # 接收
        # 验证
        # 处理
        # 1、生成图片的文本、数据
        text, code, image = captcha.generate_captcha()
        # 2、保存图片文本，用于后续与用户输入值对比
        redis_cli = get_redis_connection('image_code')
        redis_cli.setex(uuid, constans.IMAGE_CODE_EXPIRES, code)
        # 响应：输出图片数据
        return HttpResponse(image, content_type='image/png')
