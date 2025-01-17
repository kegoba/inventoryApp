
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import InventorySerializer
from .repositories import InventoryRepository
from .task import generate_report

class InventoryViewSet(viewsets.ViewSet):

    def list(self, request):
        products = InventoryRepository.get_all_products()
        serializer = InventorySerializer(products, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        product = InventoryRepository.get_product_by_id(pk)
        if not product:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = InventorySerializer(product)
        return Response(serializer.data)



    def update(self, request, pk=None):
        result = InventoryRepository.update_inventory(pk, request.data)
        if isinstance(result, dict) and 'error' in result:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

        return Response(InventorySerializer(result).data)


    @action(detail=False, methods=['get'])
    def low_stock_alert(self, request):
        low_stock_products = InventoryRepository.check_low_stock_products()
        serializer = InventorySerializer(low_stock_products, many=True)
        return Response(serializer.data)



class ReportViewSet(viewsets.ViewSet):
    def list(self, request):
        try:
            report_data = generate_report()
            return Response({
                "message": "Report generated successfully",
                "data": report_data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "error": "An error occurred while generating the report",
                "details": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


