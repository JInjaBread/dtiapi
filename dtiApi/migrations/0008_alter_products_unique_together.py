# Generated by Django 4.0.4 on 2022-05-28 07:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dtiApi', '0007_alter_data_publish_at'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='products',
            unique_together={('product_name', 'product_unit')},
        ),
    ]