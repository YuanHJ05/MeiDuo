# 创建项目
- 创建git仓库
    - 在gitbhu里面新建项目
    - 创建.gitignore文件（忽略上传文件）
    - 克隆仓库
        ```
        git clone https://github.com/YuanHJ05/MeiDuo.git
        ```
- 创建项目
    - 创建虚拟环境
        ```
        pip install pipenv
    - 激活虚拟环境
        ```
        pipenv shell
    - 安装Django
        ```
        pipenv install django==2.0
    - 创建Django项目（meiduo_mall）
        ```
        django-admin startproject meiduo_mall
# 配置
- 修改配置文件
    - 新建python packge包(settings)
    - 剪切原settings.py 到 settings 包下，并更改文件名字为dev_settings.py
    - 修改manage.py，指定开发配置文件
        ```
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "meiduo_mall.settings.dev_settings")  # 指定读取配置文件的路径
- 配置Jinja2模板
    - 安装Jinja2
        ``` 
        pipenv install Jinja2
    - 配置Jinja2模板（dev_settings.py）
        ```
        TEMPLATES = [
                    {
                        # 'BACKEND': 'django.template.backends.django.DjangoTemplates',
                        'BACKEND': 'django.template.backends.jinja2.Jinja2',
                        'DIRS': [os.path.join(BASE_DIR,'templates')],
                        'APP_DIRS': True,
                        'OPTIONS': {
                            'context_processors': [
                                'django.template.context_processors.debug',
                                'django.template.context_processors.request',
                                'django.contrib.auth.context_processors.auth',
                                'django.contrib.messages.context_processors.messages',
                            ],
                             # 补充Jinja2模板引擎环境
                            'environment': 'meiduo_mall.utils.jinja2_env.jinja2_environment', 
                        },
                    },
                ]
    - 创建templates文件夹
    - 创建utils包
    - 在utils包下创建jinja2_env.py
        ```
        from django.contrib.staticfiles.storage import staticfiles_storage
        from django.urls import reverse
        from jinja2 import Environment


        def jinja2_environment(**options):
            env = Environment(**options)
            env.globals.update({
                'static': staticfiles_storage.url,
                'url': reverse,
            })
            return env


        """
        确保可以使用Django模板引擎中的{% url('') %} {% static('') %}这类的语句 
        """
- 配置mysql数据库
    - mysql创建数据库meiduo_mall
        ```
        CREATE DATABASE meiduo_mall CHARSET=utf8;
    - dev_settings.py
        ```
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql', # 数据库引擎
                'HOST': '127.0.0.1', # 数据库主机
                'PORT': 3306, # 数据库端口
                'USER': 'root', # 数据库用户名
                'PASSWORD': '123456', # 数据库用户密码
                'NAME': 'meiduo_mall' # 数据库名字
            },
        }
    - 安装pymysql
        ```
        pipenv install pymysql
    - 在项目__init__.py中
        ```
        import pymysql
        pymysql.install_as_MySQLdb()
- 配置redis数据库
    - 安装拓展包
        ```
        pipenv install django-redis
    - dev_settigs.py添加配置文件
        ```
        # 使用redis缓存，配置session使用redis
        CACHES = {
            "default": { # 默认
                "BACKEND": "django_redis.cache.RedisCache",
                "LOCATION": "redis://127.0.0.1:6379/0",  # 可改:ip,port,db
                "OPTIONS": {
                    "CLIENT_CLASS": "django_redis.client.DefaultClient",
                }
            },
            "session": { # session
                "BACKEND": "django_redis.cache.RedisCache",
                "LOCATION": "redis://127.0.0.1:6379/1",
                "OPTIONS": {
                    "CLIENT_CLASS": "django_redis.client.DefaultClient",
                }
            },
        }
        #指定session的保存方案
        SESSION_ENGINE = "django.contrib.sessions.backends.cache"
        SESSION_CACHE_ALIAS = "session"
- 配置工程日志
    - dev_settiongs.py
        ```
        LOGGING = {
            'version': 1,
            'disable_existing_loggers': False,  # 是否禁用已经存在的日志器
            'formatters': {  # 日志信息显示的格式
                'verbose': {
                    'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
                },
                'simple': {
                    'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
                },
            },
            'filters': {  # 对日志进行过滤
                'require_debug_true': {  # django在debug模式下才输出日志
                    '()': 'django.utils.log.RequireDebugTrue',
                },
            },
            'handlers': {  # 日志处理方法
                'console': {  # 向终端中输出日志
                    'level': 'INFO',
                    'filters': ['require_debug_true'],
                    'class': 'logging.StreamHandler',
                    'formatter': 'simple'
                },
                'file': {  # 向文件中输出日志
                    'level': 'INFO',
                    'class': 'logging.handlers.RotatingFileHandler',
                    'filename': os.path.join(os.path.dirname(BASE_DIR), 'logs/meiduo.log'),  # 日志文件的位置
                    'maxBytes': 300 * 1024 * 1024,
                    'backupCount': 10,
                    'formatter': 'verbose'
                },
            },
            'loggers': {  # 日志器
                'django': {  # 定义了一个名为django的日志器
                    'handlers': ['console', 'file'],  # 可以同时向终端与文件中输出日志
                    'propagate': True,  # 是否继续传递日志信息
                    'level': 'INFO',  # 日志器接收的最低日志级别
                },
            }
        }
    - 创建日志目录 logs
- 创建静态文件static
    - 静态文件访问路径
        ```
        # 配置静态文件加载路径
        STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
- 目录结构
    - meiduo_mall
        - apps: 应用目录
        - libs: 第三方包
        - settiongs: 配置文件目录
        - static: 静态文件目录
        - templates: 模板文件目录
        - utils: 自己封装的代码
# 用户模块
- 在apps目录下创建应用app
    ```
    $ cd ~/projects/meiduo_project/meiduo_mall/meiduo_mall/apps
    $ python ../../manage.py startapp users
- 指定应用的导包路径为meiduo_mall/apps(dev_settings.py)
    ```
    sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
- 注册app
    ```
    INSTALLED_APPS = [
    ......
    'users'
    ]
- 在apps目录上，右键，Mark Director as 选择Sources Root
- 用户模型类
    - 继承AbstractUser
        ```
        from django.db import models
        from django.contrib.auth.models import AbstractUser


        # Create your models here.
        class User(AbstractUser):
            mobile = models.CharField(max_length=11)
    - 一定要指定项目用户模型类在dev_settings.py里面
        ```
        # AUTH_USER_MODEL = '应用名.模型类名'
        AUTH_USER_MODEL = 'users.User'