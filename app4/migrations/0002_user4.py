# Generated by Django 2.2.5 on 2022-08-09 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app4', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User4',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32, verbose_name='用户名')),
                ('password', models.CharField(max_length=12, verbose_name='密码')),
                ('email', models.CharField(max_length=50, verbose_name='用户邮箱')),
            ],
        ),
    ]
