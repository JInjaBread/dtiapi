# Generated by Django 4.0.4 on 2022-06-12 10:21

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Concern',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('receipt_image', models.ImageField(upload_to='complains/')),
                ('complainant_email', models.CharField(max_length=255)),
                ('complains', models.CharField(max_length=255)),
                ('concern_adress', models.BooleanField(default=False)),
                ('publish_at', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_file', models.FileField(upload_to='pdf/')),
                ('publish_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=255)),
                ('supermarket_price', models.FloatField()),
                ('wetmarket_price', models.FloatField()),
                ('product_image', models.ImageField(upload_to='images/')),
                ('product_unit', models.CharField(max_length=255)),
                ('product_description', models.CharField(max_length=255)),
                ('main_category', models.CharField(choices=[('BASIC NECESSITIES', 'BASIC NECESSITIES'), ('PRIME COMMODITIES', 'PRIME COMMODITIES')], max_length=255)),
                ('product_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category', to='dtiApi.productcategory')),
            ],
            options={
                'unique_together': {('product_name', 'product_unit')},
            },
        ),
    ]
