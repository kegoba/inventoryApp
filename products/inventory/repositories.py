# products/repositories.py

from products.models import Product,Supplier
from .serializers import InventorySerializer
from django.db import transaction
from django.db.models import F

class InventoryRepository:
    @staticmethod
    def get_all_products():
        return Product.objects.all()

    @staticmethod
    def get_product_by_id(product_id):
        return Product.objects.filter(id=product_id).first()

    @staticmethod
    def update_inventory(product, data):

        if 'supplier_id' not in data:
            return {"error": "Supplier id must be included"}

        try:
            supplier = Supplier.objects.get(id=data['supplier_id'])
            product.supplier_id = supplier  
        except Supplier.DoesNotExist:
            return {"error": "Supplier with the given ID does not exist"}

        if 'quantity' in data:
            new_quantity = data['quantity']
            if new_quantity < 0:
                return {"error": "Quantity cannot be negative"}
            product.quantity = new_quantity

        for field, value in data.items():
            if field != 'quantity' and field != 'supplier_id':
                setattr(product, field, value)
        print(product,"products")
        product.save()
        return product

    @staticmethod
    def check_low_stock_products():
        return Product.objects.filter(quantity__lte=F('low_stock_threshold'))
