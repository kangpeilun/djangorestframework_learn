# Generated by Django 2.2.5 on 2022-08-09 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book4',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='书籍名称')),
                ('price', models.IntegerField(verbose_name='价格')),
                ('pub_date', models.DateField(verbose_name='出版日期')),
            ],
        ),
        migrations.CreateModel(
            name='PublishMent4',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='出版社名称')),
                ('address', models.CharField(max_length=32, verbose_name='出版社地址')),
            ],
        ),
    ]
