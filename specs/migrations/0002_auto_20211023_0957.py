# Generated by Django 3.1.7 on 2021-10-23 06:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_auto_20211023_0957'),
        ('specs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='featurevalidator',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.category', verbose_name='Категория'),
        ),
        migrations.AddField(
            model_name='productfeatures',
            name='feature',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='specs.categoryfeature', verbose_name='Характеристика'),
        ),
        migrations.AddField(
            model_name='productfeatures',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.product', verbose_name='Товар'),
        ),
        migrations.AlterField(
            model_name='featurevalidator',
            name='feature_key',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='specs.categoryfeature', verbose_name='Ключ характеристики'),
        ),
    ]
