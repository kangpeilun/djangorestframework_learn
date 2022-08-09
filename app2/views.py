from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.generics import GenericAPIView

from app2.models import Book2, PublishMent

# Create your views here.
class BookSerializers(serializers.ModelSerializer):
    '''ModelSerializer序列化器中已经实现了create和update方法(不需要再重写一遍)，
    直接serializer.save()用即可，规律和之前一样
    '''
    date = serializers.DateField(source='pub_date')     # 如果想要取别名，需要额外去定义
    class Meta:
        model = Book2    # 对哪个模型进行序列化
        # fields = ["title", "price", "pub_date"]     # 对指定字段进行序列化
        # fields = "__all__"     # 对所有字段进行序列化
        '''
        因为新定义了 date别名，故原来的pub_date就不需要再包含在fields内了
        exclude 表示除了 pub_date 字段不参与序列化的过程，其他的都参与
        fields 和 exclude不能一起使用
        '''
        exclude = ["pub_date"]


class PublishMentSerializers(serializers.ModelSerializer):
    class Meta:
        model = PublishMent
        fields = "__all__"


'''
GenericAPIView继承自APIView，主要增加了操作序列化器和数据库查询的方法
作用是为下面Minxin扩展类的执行提供方法支持。通常在使用时，可搭配一个或多个Minxin扩展类
get_serializer_class(self): 获取序列化器类名
    当出现一个视图类中调用多个序列化器时，那么可以通过条件判断在get_serializer_class方法中通过返回不同的序列化器类名，
    就可以让视图函数执行不同的序列化器对象了
    
get_serializer(self, args, *kwargs): 获取序列化对象
    主要用来提供给Mixin扩展类使用，如果我们在试图中想要获取序列化器对象，也可以直接调用此方法
    注意：该方法在提供序列化器对象的时候，会向序列化器对象的context属性补充三个数据：
        request、format、view，这三个数据对象可以在定义序列化器时使用
        request: 当前视图的请求对象
        view: 当前请求的类试图对象
        format: 当前请求期望返回的数据格式

get_queryset(self): 获取查询集结果
    主要用来提供给Mixin扩展类使用，是列表视图与详情视图获取数据的基础，默认返回 queryset 属性，可以重写

get_object(self): 获取单一的资源对象
    返回详情视图所需的模型类数据对象，主要用来提供给Mixin扩展类使用
    在视图中可以调用该方法获取详情信息的模型类对象
    PS：1.若详情访问的模型类对象不存在，会返回404
        2.该方法默认会使用APIView提供的check_object_permissions方法检查当前对象是否有权限被访问
'''
class BookView(GenericAPIView):
    '''
    DRF路由书写规范
    /book/      GET     查看所有资源，返回所有资源
    /book/      POST    添加资源，返回添加资源
    /book/1     GET     查看某个资源，返回这一个资源
    /book/1     PUT     编辑某个资源，返回编辑之后的这个资源
    /book/1     DELETE  删除某个资源，返回null
    '''
    # PS: 属性名必须这样写，不能改
    queryset = Book2.objects.all()
    serializer_class = BookSerializers

    def get(self, request):
        # 查看所有书籍
        # 构建序列化器对象
        # 此处的 self.get_queryset() <=> Book2.objects.all()
        #       self.get_serializer <=> BookSerializers
        # 这样做的目的是使 代码更统一，方便复用
        serializer = self.get_serializer(instance=self.get_queryset(), many=True)

        # Response 会把序列化的结果处理成一个json的格式返回，比HttpResponse 好用
        return Response(serializer.data)

    def post(self, request):
        # 添加一本书籍
        book = request.data
        print('data:', book)
        # 构建序列化器对象
        serializer = self.get_serializer(data=book, many=False)
        # 校验数据
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)    # post请求返回添加的数据本身
        else:
            return Response(serializer.errors)  # 返回出错的字段


class BookDetailView(GenericAPIView):
    '''针对单个资源操作时，另外单独写一个类, 避免GET请求两个视图函数冲突'''
    queryset = Book2.objects.all()
    serializer_class = BookSerializers

    '''
    lookup_field 用于设置根据 数据库表的哪个字段去 上面的 queryset中查找记录
    需要特别注意的是：urls.py、lookup_field、def get(self, request, id) 三处的设置要一致，否则会出错
        在下面这个例子中，三处任何一个位置的 id 都不能省
        re_path(r"book2/(?P<id>\d+)", BookDetailView.as_view())
        lookup_field = "id"
        def get(self, request, id)
    三个位置中，都需要用id，那么在使用self.get_object()时才会自动根据 数据库表中的id值，查找对应的记录
    lookup_field 的值可以修改，但修改一个地方，剩下的两个地方也要修改
    '''
    lookup_field = "id"

    def get(self, request, id):
        # 这里的id 保存着，url中最后一个 / 之后的数字
        # 查询某个记录
        # get返回的是一个模型类对象，filter返回的是一个queryset
        serializer = self.get_serializer(instance=self.get_object(), many=False)
        return Response(serializer.data)

    def put(self, request, id):
        # 编辑某个记录
        # 获取提交的更新数据
        data = request.data
        serializers = self.get_serializer(instance=self.get_object(), data=data, many=False)
        if serializers.is_valid():  # 对 data 数据进行校验
            # 校验成功，更新数据
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors)

    def delete(self, request, id):
        # 删除某个记录
        self.get_object().delete()
        return Response()


'''
使用GenericAPIView 可以写一个基类，其他别的视图类都可以继承
然后只需要修改queryset、serializer_class和lookup_field 即可实现相同的功能
大大减少代码量
'''
class PublishMentView(BookView):
    queryset = PublishMent.objects.all()
    serializer_class = PublishMentSerializers


class PublishMentDetailView(BookDetailView):
    queryset = PublishMent.objects.all()
    serializer_class = PublishMentSerializers
    lookup_field = "id"