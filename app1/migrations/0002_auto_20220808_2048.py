# Generated by Django 2.2.5 on 2022-08-08 12:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='pub_data',
            new_name='pub_date',
        ),
    ]
