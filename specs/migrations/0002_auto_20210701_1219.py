# Generated by Django 3.1.7 on 2021-07-01 09:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('specs', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='categoryfeature',
            options={'verbose_name': 'Характеристики категорий'},
        ),
        migrations.AlterModelOptions(
            name='featurevalidator',
            options={'verbose_name': 'Проверка характеристик'},
        ),
        migrations.AlterModelOptions(
            name='productfeatures',
            options={'verbose_name': 'Характеристики продуктов'},
        ),
    ]
