# Generated by Django 3.1.7 on 2021-07-13 05:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0047_auto_20210712_1606'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name_plural': 'Покупатели'},
        ),
    ]