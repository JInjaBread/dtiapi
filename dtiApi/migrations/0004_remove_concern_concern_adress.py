# Generated by Django 4.0.4 on 2022-06-12 10:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dtiApi', '0003_products_supermarket_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='concern',
            name='concern_adress',
        ),
    ]
