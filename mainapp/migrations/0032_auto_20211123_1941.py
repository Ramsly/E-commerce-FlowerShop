# Generated by Django 3.2.8 on 2021-11-23 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0031_auto_20211123_1911'),
    ]

    operations = [
        migrations.AddField(
            model_name='dislike',
            name='is_click',
            field=models.BooleanField(default=False, verbose_name='Статус'),
        ),
        migrations.AddField(
            model_name='like',
            name='is_click',
            field=models.BooleanField(default=False, verbose_name='Статус'),
        ),
    ]
