from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=32, verbose_name='书籍名称')
    price = models.IntegerField(verbose_name='价格')
    pub_date = models.DateField(verbose_name='出版日期')