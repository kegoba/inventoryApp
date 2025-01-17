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
    def update_inventory(product_id, data):
        product = Product.objects.filter(id=product_id).first()
        if not product:
            return {"error": "Product not found"}
        quantity = data.get("quantity")
        price = data.get("price")
        if quantity is not None:
            if quantity < 1:
                return {"error": "Quantity cannot be less than 1"}
            product.quantity = quantity

        if price is not None:
            if price < 1:
                return {"error": "Price cannot be less than 1"}
            product.price = price

        product.save()
        return product

    @staticmethod
    def check_low_stock_products():
        return Product.objects.filter(quantity__lte=F('low_stock_threshold'))
