# Generated by Django 3.2.8 on 2021-10-29 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0004_auto_20211029_1800'),
        ('mainapp', '0020_auto_20211029_1720'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(to='cart.OrderItem', verbose_name='Продукты '),
        ),
    ]
