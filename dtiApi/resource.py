from import_export import resources
from .models import Products

class ProductResource(resources.ModelResource):
    class meta:
        model = Products
