from django.shortcuts import render
from django.views import View
from meiduo_mall.libs.captcha.captcha import captcha
from django_redis import get_redis_connection
from . import constans
from django.http import HttpResponse, JsonResponse
from meiduo_mall.utils.response_code import RETCODE
import random
from meiduo_mall.libs.yuntongxun.sms import CCP  # 容联云通讯包


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


class SmsCodeView(View):
    def get(self, request, mobile):
        # 接收
        uuid = request.GET.get('image_code_id')
        image_code = request.GET.get('image_code')
        # 验证
        if not all([uuid, image_code]):
            return JsonResponse({'code': RETCODE.PARAMERR, 'errmsg': '参数不完整'})
        # 验证图形验证码是否正确
        # 从redis中读取之前保存的图像验证码文本
        redis_cli = get_redis_connection('image_code')
        image_code_redis = redis_cli.get(uuid)  # bytes类型
        # 如果redis中的数据过期
        if image_code_redis is None:
            return JsonResponse({'code': RETCODE.IMAGECODEERR, 'errmsg': '图像验证码已过期，点击图片换一个'})
        # 立即删除redis中图形验证码，表示这个值不能使用第二次
        redis_cli.delete(uuid)
        # 对比图形验证码
        if image_code_redis.decode().lower() != image_code.lower():  # 全部转换为小写，不区分大小分，根据业务需求来定
            return JsonResponse({'code': RETCODE.IMAGECODEERR, 'errmsg': '图像验证码错误'})
        # 处理
        # 1、生成随机6位数
        sms_code = random.randint(100000, 999999)
        # 2、存入redis
        redis_cli_sms = get_redis_connection('sms_code')
        redis_cli_sms.setex(mobile, constans.SMS_CODE_EXPIRES, sms_code)  # 键是mobile,值是sms_code
        # 发送短信
        ccp = CCP()
        ccp.send_template_sms(mobile, [sms_code, constans.SMS_CODE_EXPIRES / 60], 1)
        # print(sms_code)
        # 响应
        return JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK'})
