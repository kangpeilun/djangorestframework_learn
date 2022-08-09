from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response    # Response 会把序列化的结果处理成一个json的格式返回，比HttpResponse 好用

from app1.models import Book

# Create your views here.

class BaseLearnView(APIView):

    def get(self, request):
        # 经过APIView包装后的request是新产生的，其经过了包装，
        # 无论前端传什么样格式的数据，在后端都会被解析为 Query字典 格式，保存在request.data中
        print('data: ', request.query_params)    # request.query_param 获取get请求的参数
        return HttpResponse('APIView GET请求...')

    def post(self, request):
        print('data: ', request.data)           # request.data 获取post请求的参数
        return HttpResponse('APIView POST请求...')

    def delete(self, request):
        return HttpResponse('APIView DELETE请求...')


# class BookSerializers(serializers.Serializer):
#     '''针对模型类设计一个序列化器
#     注意：1.序列化器中的字段名称必须和 模型类中的字段名称一致，否则会报错
#         2.如果模型类中有3条字段，而序列化器中只写了其中2条字段，那么不会报错，只是 只序列化这2个字段而已
#         3.序列化器这样写，是为了 在反序列化的时候 做校验用的
#     '''
#     # id = serializers.IntegerField()     # 获取id
#     title = serializers.CharField(max_length=32)
#     price = serializers.IntegerField()
#     # source='pub_data' 可以理解为对pub_data字段取得 别名
#     # 序列化器是根据data名获取的数据，但在序列化器内部校验的时候还是用的 pub_data
#     # 即对外展示的时候用的是别名 data，但在内部处理的时候用的还是 pub_data
#     date = serializers.DateField(source='pub_date')
#
#     def create(self, validated_data):
#         # 添加数据逻辑
#         # 此处的 validated_data 为正确反序列化后的数据
#         new_book = Book.objects.create(**validated_data)
#         # 重写序列化器的create方法时，需要有一个返回值，该返回值为创建一条新纪录的 instance
#         # 之后再使用serializer.data时才能正确序列化 新创建的数据
#         return new_book
#
#     def update(self, instance, validated_data):
#         # 修改数据
#         # 此处 instance 为序列化前 数据库中查询到的数据
#         #     validated_data 为正确反序列化后的数据
#         print('update instance: ', instance, 'validated_data: ', validated_data)
#         # update更新时一定要用 serializers.validated_data 否则可能会报字段不存在的错误
#         # 切记：1.update后的返回值是 修改了多少条记录(个数)，而 不是 一个模型类对象
#         #     2.只有 queryset 数据类型才有 update方法，因此更新数据必须用 Book.objects.filter(id=id)获取数据，而不能用 .get(id=id)
#         Book.objects.filter(id=instance.id).update(**validated_data)
#         updated_book = Book.objects.get(id=instance.id)
#         # 重写序列化器的update方法时，需要有一个返回值，该返回值为 修改对应记录后的 instance
#         # 之后再使用serializer.data时才能正确序列化 修改后的数据
#         return updated_book


class BookSerializers(serializers.ModelSerializer):
    '''ModelSerializer序列化器中已经实现了create和update方法(不需要再重写一遍)，
    直接serializer.save()用即可，规律和之前一样
    '''
    date = serializers.DateField(source='pub_date')     # 如果想要取别名，需要额外去定义
    class Meta:
        model = Book    # 对哪个模型进行序列化
        # fields = ["title", "price", "pub_date"]     # 对指定字段进行序列化
        # fields = "__all__"     # 对所有字段进行序列化
        '''
        因为新定义了 date别名，故原来的pub_date就不需要再包含在fields内了
        exclude 表示除了 pub_date 字段不参与序列化的过程，其他的都参与
        fields 和 exclude不能一起使用
        '''
        exclude = ["pub_date"]



class BookView(APIView):
    '''
    DRF路由书写规范
    /book/      GET     查看所有资源，返回所有资源
    /book/      POST    添加资源，返回添加资源
    /book/1     GET     查看某个资源，返回这一个资源
    /book/1     PUT     编辑某个资源，返回编辑之后的这个资源
    /book/1     DELETE  删除某个资源，返回null
    '''
    def get(self, request):
        # 查看所有书籍
        book_list = Book.objects.all()  # 获取所有的书籍   queryset[book1, book2, ...]
        # 构建序列化器对象
        # BookSerializers(instance=, data=, many=)
        # instance参数用于 序列化 传参(参数为模型类对象)，data参数用于 反序列化 传参
        # 如果序列化多个模型类对象，many=True；反之many=False
        # 使用 serializer.data 通过函数获取序列化结果
        serializer = BookSerializers(instance=book_list, many=True)

        # Response 会把序列化的结果处理成一个json的格式返回，比HttpResponse 好用
        return Response(serializer.data)

    def post(self, request):
        # 添加一本书籍
        book = request.data
        print('data:', book)
        # 构建序列化器对象
        serializer = BookSerializers(data=book, many=False)
        # 校验数据
        # 所有符合要求的数据都会被放入 serializer.validated_data 中
        # 如果某个字段值不符合要求，错误的 key:错误原因 会被放入 serializer.errors 中
        # 所有字段都通过的时候，返回True；否则返回False
        if serializer.is_valid():
            # 校验通过，将数据插入到数据库中，所有通过校验的数据都会被保存在 serializer.validated_data 中
            # Book.objects.create(**serializer.validated_data)
            # serializer.save() 中save操作可以根据参数instance= 和 data= 来判断是进行 update()更新 还是 create()创建 操作
            # 要使用serializer.save()，就必须在序列化器中进行 重写 update或create方法
            serializer.save()
            # 前面已经通过BookSerializers进行反序列化了，所以数据已经被保存在 类中，直接使用serializer.data获取序列化结果即可
            return Response(serializer.data)    # post请求返回添加的数据本身
        else:
            return Response(serializer.errors)  # 返回出错的字段


class BookDetailView(APIView):
    '''针对单个资源操作时，另外单独写一个类, 避免GET请求两个视图函数冲突'''
    def get(self, request, id):
        # 这里的id 保存着，url中最后一个 / 之后的数字
        # 查询某个记录
        # get返回的是一个模型类对象，filter返回的是一个queryset
        book = Book.objects.get(id=id)
        serializer = BookSerializers(instance=book, many=False)
        return Response(serializer.data)

    def put(self, request, id):
        # 编辑某个记录
        # 获取提交的更新数据
        data = request.data
        # 如果是使用ModelSerializer进行序列化时 然后更新数据时，需要在序列化时 instance传入 模型类对象，即用 .get(id=id) 查询数据
        update_book = Book.objects.get(id=id)   # 获取要更新的对象
        # 因为要对数据库中已经存在的对象进行更新，因此需要进行 序列化，即需要参数instance
        # 同时又需要将用户提交的更新数据 存到数据库，因此需要进行 反序列化，即需要参数data
        serializers = BookSerializers(instance=update_book, data=data, many=False)
        if serializers.is_valid():  # 对 data 数据进行校验
            # 校验成功，更新数据
            # 注意：update更新时一定要用 serializers.validated_data 否则可能会报字段不存在的错误
            # 切记：1.update后的返回值是 修改了多少条记录(个数)，而 不是 一个模型类对象
            #     2.只有 queryset 数据类型才有 update方法，因此更新数据必须用 Book.objects.filter(id=id)获取数据，而不能用 .get(id=id)
            # Book.objects.filter(id=id).update(**serializers.validated_data)
            # serializers.instance = Book.objects.get(id=id)

            '''
            serializers.save()可以总结以下规律：
                1.当序列化时 同时 存在instance和data参数时，那么serializers.save()表示 对原有数据进行更新
                    其中 instance中保存着原来的数据queryset, data中保存用户提交的待更新的数据
                2.当序列化时 仅 存在data参数时，那么serializers.save()表示 添加一条新的数据
            '''
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors)


    def delete(self, request, id):
        # 删除某个记录
        Book.objects.get(id=id).delete()
        return Response()