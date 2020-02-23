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