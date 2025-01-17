from rest_framework import viewsets, status
from rest_framework.response import Response
from .repositories import SupplierRepository
from .serializers import SupplierSerializer

class SupplierViewSet(viewsets.ViewSet):
    def list(self, request):

        page = request.query_params.get('page', 1)
        per_page = request.query_params.get('per_page', 10)

        result = SupplierRepository.get_all_suppliers(page=page, per_page=per_page)
        serializer = SupplierSerializer(result["suppliers"], many=True)

        return Response({
            "products": serializer.data,
            "total_products": result["total_products"],
            "total_pages": result["total_pages"],
            "current_page": result["current_page"],
        })

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
           
            supplier = SupplierRepository.delete_supplier(pk)
       
            return Response(supplier, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
