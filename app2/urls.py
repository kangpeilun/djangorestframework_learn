# -*- coding: utf-8 -*-
# date: 2022/8/8 23:05
# Project: djangorestframework_learn
# File Name: urls.py
# Description: 
# Author: Anefuer_kpl
# Email: 374774222@qq.com

from django.urls import path, re_path
from app2.views import BookView, BookDetailView, PublishMentView, PublishMentDetailView

urlpatterns = [
    # 注意：若有同名路由，且另一个路由用于 正则传参，那么第一个 路由不能用 re_path，否则会报错
    path(r"book2/", BookView.as_view(), name='book'),  # 操纵所有记录
    # 注意：通过url保存参数并传给视图函数，传的值需要用 () 包起来，否则识别不了
    # book2/(\d+) 这种url写法叫 无名分组，其按照位置参数传参
    re_path(r"book2/(?P<id>\d+)", BookDetailView.as_view(), name='bookdetail'),  # 操纵某条记录

    path(r"publish2/", PublishMentView.as_view()),
    re_path(r"publish2/(?P<id>\d+)", PublishMentDetailView.as_view())
]
