# -*- coding: utf-8 -*-
# date: 2022/8/9 19:14
# Project: djangorestframework_learn
# File Name: urls.py
# Description: 
# Author: Anefuer_kpl
# Email: 374774222@qq.com

from django.urls import path, re_path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from app4.views import BookView

router = routers.DefaultRouter()
router.register('book4', BookView, basename='book')

urlpatterns = [
    # 获取Token接口
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify/', TokenVerifyView.as_view(), name='token_verify')
]

urlpatterns += router.urls