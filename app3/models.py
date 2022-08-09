from django.db import models

# Create your models here.
class Book3(models.Model):
    title = models.CharField(max_length=32, verbose_name='书籍名称')
    price = models.IntegerField(verbose_name='价格')
    pub_date = models.DateField(verbose_name='出版日期')


class PublishMent3(models.Model):
    name = models.CharField(max_length=32, verbose_name='出版社名称')
    address = models.CharField(max_length=32, verbose_name='出版社地址')