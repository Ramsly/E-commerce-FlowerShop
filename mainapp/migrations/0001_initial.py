# Generated by Django 3.1.7 on 2021-10-23 06:52

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Имя категории')),
                ('image', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Изображение категории')),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('f_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Имя')),
                ('l_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Фамилия')),
                ('image', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Изображение')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Почта')),
                ('phone_number', models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('address', models.CharField(blank=True, max_length=255, null=True, verbose_name='Адрес')),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'verbose_name_plural': 'Покупатели',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=255, verbose_name='Наименование')),
                ('slug', models.SlugField(unique=True)),
                ('image', models.ImageField(upload_to='flowers/', verbose_name='Изображение')),
                ('description', models.TextField(null=True, verbose_name='Описание')),
                ('price', models.FloatField(default=0, verbose_name='Цена')),
                ('shipping_price', models.IntegerField(default=0, verbose_name='Стоимость доставки')),
                ('sale_value', models.FloatField(default=0, help_text='В процентах. Значок процента не ставить!', verbose_name='Величина скидки')),
                ('available', models.BooleanField(default=True, verbose_name='Наличие товара')),
            ],
            options={
                'verbose_name': 'Товары',
                'verbose_name_plural': 'Товары',
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=15, verbose_name='IP адрес')),
            ],
            options={
                'verbose_name': 'Рейтинг',
                'verbose_name_plural': 'Рейтинги',
            },
        ),
        migrations.CreateModel(
            name='RatingStar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.SmallIntegerField(default=0, verbose_name='Значение')),
            ],
            options={
                'verbose_name': 'Звезда рейтинга',
                'verbose_name_plural': 'Звезды рейтинга',
                'ordering': ['-value'],
            },
        ),
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_created=True, auto_now=True, null=True, verbose_name='Дата комментария')),
                ('name', models.CharField(max_length=100, null=True, verbose_name='Имя')),
                ('comment', models.TextField(max_length=5000, null=True, verbose_name='Комментарий')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.product', verbose_name='Цветы')),
            ],
            options={
                'verbose_name_plural': 'Отзывы',
                'ordering': ['-time'],
            },
        ),
    ]
