# Generated by Django 3.1.7 on 2021-05-19 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0027_auto_20210516_0939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='sale_value',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='В процентах. Значок процента не ставить!', max_digits=9, null=True, verbose_name='Величина скидки'),
        ),
    ]
