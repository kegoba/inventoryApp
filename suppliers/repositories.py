
from .models import Supplier
from .serializers import SupplierSerializer

class SupplierRepository:
    @staticmethod
    def get_all_suppliers():
        return Supplier.objects.all()

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
    def delete_supplier(supplier):
        supplier.delete()
