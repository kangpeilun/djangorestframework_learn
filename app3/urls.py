# -*- coding: utf-8 -*-
# date: 2022/8/9 13:22
# Project: djangorestframework_learn
# File Name: urls.py
# Description: 
# Author: Anefuer_kpl
# Email: 374774222@qq.com
from django.urls import path, re_path
from rest_framework import routers

from app3.views import BookView, BookDetailView, PublishMentView

router = routers.DefaultRouter()
'''
    router.register('publish3', PublishMentView) 这种写法 
        <=> 等价于
    path(r"publish3/", PublishMentView.as_view({"get": "get_all", "post": "add_object"})),
    re_path(r"publish3/(?P<id>\d+)", PublishMentView.as_view({"get": "get_object", "put": "update_object", "delete": "delete_object"}))
        或
    path(r"publish3/", PublishMentView.as_view({"get": "list", "post": "create"})),
    re_path(r"publish3/(?P<id>\d+)", PublishMentView.as_view({"get": "retrieve", "put": "update", "delete": "destroy"}))
    
    其本质是替代了 视图类.as_view() 中 映射函数 的书写, 同样是要求和 ViewSet、GenericViewSet、ModelViewSet 联合使用
'''
router.register('publish3', PublishMentView)

urlpatterns = [
    path(r"book3/", BookView.as_view()),
    re_path(r"book3/(?P<id>\d+)", BookDetailView.as_view()),

    # 切记只有 继承了 ViewSet 的视图类，其 as_view中才可以加参数
    # 因为视图类继承了 ViewSet类，那么在写Url时，as_view可以传入一个字典，用于分发映射
    # 如{"get": "get_all", "post": "add_object"}
    # 就是在这个路由下，将get请求 映射给 PublishMentView类下的get_all方法处理；post请求 映射给 PublishMentView类下的add_object方法处理
    # path(r"publish3/", PublishMentView.as_view({"get": "get_all", "post": "add_object"})),
    # re_path(r"publish3/(?P<id>\d+)", PublishMentView.as_view({"get": "get_object", "put": "update_object", "delete": "delete_object"}))

    # GenericViewSet 以及定义好的 ListModelMixin, CreateModelMixin, UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin 方法
    # 直接使用Mixin混合类中定义好的方法 作为分发映射即可，可以极大的减少代码量
    # path(r"publish3/", PublishMentView.as_view({"get": "list", "post": "create"})),
    # re_path(r"publish3/(?P<id>\d+)", PublishMentView.as_view({"get": "retrieve", "put": "update", "delete": "destroy"}))
]

urlpatterns += router.urls  # 此处必须要在 urlpatterns 中添加注册的路由