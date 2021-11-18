# Generated by Django 3.2.8 on 2021-11-16 06:32

import django.contrib.postgres.search
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0028_alter_product_search_vector'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='search_vector',
            field=django.contrib.postgres.search.SearchVectorField(default=models.CharField(db_index=True, max_length=255, verbose_name='Наименование'), editable=False, null=True),
        ),
    ]