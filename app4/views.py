from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework import authentication
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenViewBase

from app4.models import Book4, PublishMent4, User4



# Create your views here.
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book4
        fields = "__all__"


class PublishMentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublishMent4
        fields = "__all__"


class BookView(ModelViewSet):
    queryset = Book4.objects.all()
    serializer_class = BookSerializer
