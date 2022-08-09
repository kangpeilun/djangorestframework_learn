# -*- coding: utf-8 -*-
# date: 2022/8/8 9:37
# Project: djangorestframework_learn
# File Name: urls.py
# Description: 
# Author: Anefuer_kpl
# Email: 374774222@qq.com

from django.urls import path, re_path
from app1.views import BaseLearnView, BookView, BookDetailView

urlpatterns = [
    path("base/", BaseLearnView.as_view(), name='base'),

    # 注意：若有同名路由，且另一个路由用于 正则传参，那么第一个 路由不能用 re_path，否则会报错
    path(r"book/", BookView.as_view(), name='book'),  # 操纵所有记录
    # 注意：通过url保存参数并传给视图函数，传的值需要用 () 包起来，否则识别不了
    re_path(r"book/(\d+)", BookDetailView.as_view(), name='bookdetail'),   # 操纵某条记录
]