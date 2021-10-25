# Generated by Django 3.1.7 on 2021-10-24 12:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryFeature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature_name', models.CharField(max_length=50, verbose_name='Имя ключа для категории')),
                ('feature_filter_name', models.CharField(max_length=50, verbose_name='Имя для фильтра')),
                ('unit', models.CharField(blank=True, max_length=50, null=True, verbose_name='Единица измерения')),
            ],
            options={
                'verbose_name': 'Характеристики категорий',
            },
        ),
        migrations.CreateModel(
            name='ProductFeatures',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=255, verbose_name='Значение')),
                ('feature', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='specs.categoryfeature', verbose_name='Характеристика')),
            ],
            options={
                'verbose_name': 'Характеристики продуктов',
            },
        ),
        migrations.CreateModel(
            name='FeatureValidator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valid_feature_value', models.CharField(max_length=100, verbose_name='Валидное значение')),
                ('feature_key', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='specs.categoryfeature', verbose_name='Ключ характеристики')),
            ],
            options={
                'verbose_name': 'Проверка характеристик',
            },
        ),
    ]
