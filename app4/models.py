from django.db import models

class User4(models.Model):
    username = models.CharField(max_length=32, verbose_name='用户名')
    password = models.CharField(max_length=12, verbose_name='密码')
    email = models.CharField(max_length=50, verbose_name='用户邮箱')

# Create your models here.
class Book4(models.Model):
    title = models.CharField(max_length=32, verbose_name='书籍名称')
    price = models.IntegerField(verbose_name='价格')
    pub_date = models.DateField(verbose_name='出版日期')


class PublishMent4(models.Model):
    name = models.CharField(max_length=32, verbose_name='出版社名称')
    address = models.CharField(max_length=32, verbose_name='出版社地址')