# products/repositories.py

from .models import Product
from .serializers import ProductSerializer
from suppliers.models import Supplier
from django.db import transaction
from django.db.models import F

class ProductRepository:
    @staticmethod
    def get_all_products():
        return Product.objects.all()

    @staticmethod
    def get_product_by_id(product_id):
        return Product.objects.filter(id=product_id).first()

    @staticmethod
    def create_product(data):
        supplier_id = data.get('supplier_id')
        if supplier_id and not Supplier.objects.filter(id=supplier_id).exists():
            return {"error": "Supplier does not exist"}
        quantity = data.get('quantity', 0)
        if quantity < 0:
            return {"error": "Quantity cannot be negative"}

        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return serializer
        return serializer.errors

    @staticmethod
    def update_product(product, data):
        if 'quantity' in data:
            new_quantity = data['quantity']
            if new_quantity < 0:
                return {"error": "Quantity cannot be negative"}
            product.quantity = new_quantity
        
        for field, value in data.items():
            if field != 'quantity': 
                setattr(product, field, value)

        product.save()
        return product

    @staticmethod
    def delete_product(product):
        product.delete()

    @staticmethod
    def update_inventory(product_id, quantity):
        product = Product.objects.filter(id=product_id).first()
        if product:
            if quantity < 0:
                return {"error": "Quantity cannot be negative"}
            product.quantity = quantity
            product.save()
            return product
        return {"error": "Product not found"}

    @staticmethod
    def check_low_stock_products():
        return Product.objects.filter(quantity__lte=F('low_stock_threshold'))
