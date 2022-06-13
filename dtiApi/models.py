from django.db import models
from django.utils import timezone

class ProductCategory(models.Model):
    category_name = models.CharField(max_length=255)

    def __str__(self):
        return self.category_name

class Products(models.Model):

    MAIN_CATEGORY = [
        ('BASIC NECESSITIES', 'BASIC NECESSITIES'),
        ('PRIME COMMODITIES', 'PRIME COMMODITIES'),
    ]
    product_name = models.CharField(max_length=255)
    supermarket_price = models.FloatField()
    wetmarket_price = models.FloatField()
    product_image = models.ImageField(upload_to ='images/')
    product_unit = models.CharField(max_length=255)
    product_description = models.CharField(max_length=255)
    main_category = models.CharField(max_length=255, choices=MAIN_CATEGORY)
    product_category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name="category")

    class Meta:
        unique_together = ('product_name', 'product_unit',)

    def __str__(self):
        return self.product_name

class Concern(models.Model):
    receipt_image = models.ImageField(upload_to='complains/')
    complainant_email = models.CharField(max_length=255)
    complains = models.CharField(max_length=255)
    concern_adress = models.BooleanField(default = False)
    publish_at = models.DateTimeField(auto_now_add=True)

class Data(models.Model):
    data_file = models.FileField(upload_to='pdf/')
    publish_at = models.DateTimeField(default=timezone.now)
