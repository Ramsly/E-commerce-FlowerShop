# Generated by Django 3.1.7 on 2021-10-25 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0008_auto_20211024_1811'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='f_name',
            field=models.CharField(default='', max_length=255, verbose_name='Имя'),
        ),
        migrations.AddField(
            model_name='customer',
            name='l_name',
            field=models.CharField(default='', max_length=255, verbose_name='Фамилия'),
        ),
    ]
