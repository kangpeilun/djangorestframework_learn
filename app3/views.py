from django.shortcuts import render
from rest_framework import serializers
from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, \
    ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveDestroyAPIView, \
    RetrieveUpdateAPIView, DestroyAPIView, UpdateAPIView  # 这样可以理解为，只进行某几种操作，方便控制，比如只进行查看，只进行查看和删除 等等
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.viewsets import ViewSet, ModelViewSet, GenericViewSet
from rest_framework.response import Response

from app3.models import Book3, PublishMent3

# Create your views here.

class BookSerializers(serializers.ModelSerializer):
    '''ModelSerializer序列化器中已经实现了create和update方法(不需要再重写一遍)，
    直接serializer.save()用即可，规律和之前一样
    '''
    date = serializers.DateField(source='pub_date')     # 如果想要取别名，需要额外去定义
    class Meta:
        model = Book3    # 对哪个模型进行序列化
        # fields = "__all__"
        exclude = ["pub_date"]


class PublishMentSerializers(serializers.ModelSerializer):
    class Meta:
        model = PublishMent3
        fields = "__all__"

'''
    增删该查查 这五个方法全部封装在了 
    ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
    这5个类中，使用时，只需要继承这些类，然后调用其中封装好的方法即可
    进一步简化了GenericAPIView的书写
'''
class BookView(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = Book3.objects.all()
    serializer_class = BookSerializers

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


class BookDetailView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    queryset = Book3.objects.all()
    serializer_class = BookSerializers
    lookup_field = "id"

    def get(self, request, id):
        return self.retrieve(request)

    def put(self, request, id):
        return self.update(request)

    def delete(self, request, id):
        return self.destroy(request)

'''
    Mixin混合类再封装
    ListCreateAPIView将 
        ListModelMixin, CreateModelMixin, GenericAPIView, get, post 这3个类以及2个方法封装在一起
    RetrieveUpdateDestroyAPIView将 
        RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView, get, put, delete 这4个类以及3个方法封装在一起
'''
# class PublishMentView(ListCreateAPIView):
#     queryset = PublishMent3.objects.all()
#     serializer_class = PublishMentSerializers
#
# class PublishMentDetailView(RetrieveUpdateDestroyAPIView):
#     queryset = PublishMent3.objects.all()
#     serializer_class = PublishMentSerializers
#     lookup_field = "id"

# 下面是我自己写的另一种封装方法，上下两种方法其核心其实差不多
'''
    也可以使用下面的封装方法
    直接继承BookView基类，只需要更改其中的queryset、serializer_class和lookup_field即可
'''
# class PublishMentView(BookView):
#     queryset = PublishMent3.objects.all()
#     serializer_class = PublishMentSerializers
#
# class PublishMentDetailView(BookDetailView):
#     queryset = PublishMent3.objects.all()
#     serializer_class = PublishMentSerializers
#     lookup_field = "id"


'''ViewSet: 在APIView的基础上，重新构建了分发机制
    将 增删改查查 这5个方法 全部放在一个类中实现，而不用写两个类 分开写
'''
# class PublishMentView(ViewSet):
#
#     def get_all(self, request):
#         return Response('查询所有数据')
#
#     def add_object(self, request):
#         return Response('添加一条资源')
#
#     def get_object(self, request, id):
#         return Response('获取一条资源')
#
#     def update_object(self, request, id):
#         return Response('更新一条资源')
#
#     def delete_object(self, request, id):
#         return Response('删除一条资源')


'''GenericViewSet: 在GenericAPIView的基础上，重新构建了分发机制
    将 增删改查查 这5个方法 全部放在一个类中实现，而不用写两个类 分开写
'''
# class PublishMentView(GenericViewSet, ListModelMixin, CreateModelMixin, UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin):
#     queryset = PublishMent3.objects.all()
#     serializer_class = PublishMentSerializers
#     lookup_field = "id"

'''这两种写法是等价的，ModelViewSet是对Mixin中所有类的封装
    class PublishMentView(ModelViewSet) 
                <=> 
    class PublishMentView(GenericViewSet, ListModelMixin, CreateModelMixin, UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin)
'''
class PublishMentView(ModelViewSet):
    queryset = PublishMent3.objects.all()
    serializer_class = PublishMentSerializers
    lookup_field = "id"