
from products.models import Supplier
from .serializers import SupplierSerializer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger





class SupplierRepository:
    @staticmethod
    def get_all_suppliers(page, per_page):
      
        suppliers = Supplier.objects.all()
        paginator = Paginator(suppliers, per_page)
        try:
            paginated_suppliers = paginator.page(page)
        except PageNotAnInteger:
            paginated_suppliers = paginator.page(1)
        except EmptyPage:
            paginated_suppliers = []

        return {
            "suppliers": paginated_suppliers.object_list,
            "total_products": paginator.count,
            "total_pages": paginator.num_pages,
            "current_page": page,
        }

    @staticmethod
    def get_supplier_by_id(supplier_id):
        return Supplier.objects.filter(id=supplier_id).first()

    @staticmethod
    def create_supplier(data):
        serializer = SupplierSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return serializer
        return serializer.errors
       

    @staticmethod
    def update_supplier(supplier, data):
        for field, value in data.items():
            setattr(supplier, field, value)
        supplier.save()
        return supplier

    @staticmethod
    def delete_supplier(product_id):
        product = Supplier.objects.get(id=product_id)
        if product:  
            product.delete()
            return {"success": "deleted successfully"}
        return {"error": "supplier not found"}

