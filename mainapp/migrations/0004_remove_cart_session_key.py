# Generated by Django 3.1.7 on 2021-04-13 15:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_cart_session_key'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='session_key',
        ),
    ]
