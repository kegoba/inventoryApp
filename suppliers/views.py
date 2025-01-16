from rest_framework import viewsets, status
from rest_framework.response import Response
from .repositories import SupplierRepository
from .serializers import SupplierSerializer

class SupplierViewSet(viewsets.ViewSet):
    def list(self, request):
        try:
            suppliers = SupplierRepository.get_all_suppliers()
            serializer = SupplierSerializer(suppliers, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

    def retrieve(self, request, pk=None):
        try:
            supplier = SupplierRepository.get_supplier_by_id(pk)
            if not supplier:
                return Response({"error": "Supplier not found"}, status=404)
            serializer = SupplierSerializer(supplier)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

    def create(self, request):
        try:
            serializer = SupplierRepository.create_supplier(request.data)
            if isinstance(serializer, SupplierSerializer):
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer, status=400)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

    def update(self, request, pk=None):
        try:
            supplier = SupplierRepository.get_supplier_by_id(pk)
            if not supplier:
                return Response({"error": "Supplier not found"}, status=404)
            updated_supplier = SupplierRepository.update_supplier(supplier, request.data)
            serializer = SupplierSerializer(updated_supplier)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

    def destroy(self, request, pk=None):
        try:
            supplier = SupplierRepository.get_supplier_by_id(pk)
            if not supplier:
                return Response({"error": "Supplier not found"}, status=404)
            SupplierRepository.delete_supplier(supplier)
            return Response({"message": "Supplier deleted successfully"}, status=204)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
