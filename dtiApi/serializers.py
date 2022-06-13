from rest_framework import serializers, permissions
from drf_extra_fields.fields import Base64ImageField
from .models import Products,ProductCategory, Concern, Data


class ConcernSerializers(serializers.ModelSerializer):
    receipt_image = Base64ImageField()
    class Meta:
        model = Concern
        fields= ('receipt_image','complainant_email', 'complains')

class ProductSerializer(serializers.ModelSerializer):
    concern = ConcernSerializers(many=True, read_only=True)
    main_category = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = Products
        fields = '__all__'

class ProductCategorySerealizers(serializers.ModelSerializer):
    product = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = ProductCategory
        fields = '__all__'

class DataSerializer(serializers.ModelSerializer):

    class Meta:
        model = Data
        fields = '__all__'
