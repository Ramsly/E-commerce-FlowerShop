# Generated by Django 3.2.8 on 2021-10-30 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('specs', '0002_auto_20211025_1051'),
        ('mainapp', '0022_auto_20211030_0837'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name_plural': 'Заказы'},
        ),
        migrations.AlterField(
            model_name='product',
            name='features',
            field=models.ManyToManyField(blank=True, related_name='features_for_product', to='specs.ProductFeatures', verbose_name='Характеристика товара'),
        ),
    ]