# Generated by Django 4.0.4 on 2022-06-12 10:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dtiApi', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='products',
            name='supermarket_price',
        ),
    ]
