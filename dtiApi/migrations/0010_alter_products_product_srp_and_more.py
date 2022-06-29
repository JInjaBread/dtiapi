# Generated by Django 4.0.4 on 2022-06-28 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dtiApi', '0009_products_product_srp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='product_srp',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='products',
            name='supermarket_price',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='products',
            name='wetmarket_price',
            field=models.FloatField(default=0.0),
        ),
    ]
