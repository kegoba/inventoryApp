# products/repositories.py

from products.models import Product,Supplier
from .serializers import ProductSerializer, FileUploadSerializer
from django.db import transaction
from django.db.models import F
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class ProductRepository:
    @staticmethod
    def get_all_products(page, per_page, name=None, quantity=None, price=None):

    
        products = Product.objects.all()
        if name:
            products = products.filter(name__icontains=name)
        if quantity is not None:
            products = products.filter(quantity=quantity)
        if price is not None:
            products = products.filter(price=price) 

        paginator = Paginator(products, per_page)

        try:
            paginated_products = paginator.page(page)
        except PageNotAnInteger:
            paginated_products = paginator.page(1)
        except EmptyPage:
            paginated_products = []

        return {
            "products": paginated_products.object_list,
            "total_products": paginator.count,
            "total_pages": paginator.num_pages,
            "current_page": page,
        }
    @staticmethod
    def get_product_by_id(product_id):
        return Product.objects.filter(id=product_id).first()

    @staticmethod
    def create_product(data):
        supplier_id = data.get('supplier_id')
        #print(supplier_id)
        if supplier_id and not Supplier.objects.filter(id=supplier_id).exists():
            return {"error": "Supplier does not exist"}
        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return serializer
        return serializer.errors

    @staticmethod
    def update_product(product, data):
    
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

        product.save()
        return product

    @staticmethod
    def delete_product(product_id):
        product = Product.objects.get(id=product_id)
        if product:  
            product.delete()
            return {"success": "deleted successfully"}
        return {"error": "Product not found"}

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
    def check_low_stock_products(page, per_page):
        products = Product.objects.filter(quantity__lte=F('low_stock_threshold'))
        paginator = Paginator(products, per_page)

        try:
            paginated_products = paginator.page(page)
        except PageNotAnInteger:
            paginated_products = paginator.page(1)
        except EmptyPage:
            paginated_products = []

        return {
            "products": paginated_products.object_list,
            "total_products": paginator.count,
            "total_pages": paginator.num_pages,
            "current_page": page,
        }
        

    @staticmethod
    def bulk_create_products(products_data):

        created_products = []
        errors = []

        for row in products_data:
            serializer = FileUploadSerializer(data=row)
            if serializer.is_valid():
                created_products.append(serializer.save())
            else:
                errors.append(serializer.errors)
        
        return created_products, errors
