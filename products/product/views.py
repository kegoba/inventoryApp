
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import ProductSerializer
from .repositories import ProductRepository
from .tasks import process_csv_task

from rest_framework.parsers import MultiPartParser






def custom_404():

    response ={
        "message" : "This Url is not found",
        status : 404
    }
    return Response(response, status=404)
     

class ProductViewSet(viewsets.ViewSet):

    def list(self, request):
        page = request.query_params.get('page', 1)
        per_page = request.query_params.get('per_page', 10)
        name = request.query_params.get('name', None)
        quantity = request.query_params.get('quantity', None)
        price = request.query_params.get('price', None)
        if quantity is not None:
            quantity = int(quantity)
        if price is not None:
            price = float(price)

        result = ProductRepository.get_all_products(page, per_page,name,quantity,price)
        serializer = ProductSerializer(result["products"], many=True)

        return Response({
            "products": serializer.data,
            "total_products": result["total_products"],
            "total_pages": result["total_pages"],
            "current_page": result["current_page"],
        })
    def retrieve(self, request, pk=None):
        try:
            product = ProductRepository.get_product_by_id(pk)
            if not product:
                return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        try:
            product = ProductRepository.delete_product(pk)
            return Response(product, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request):
        try:
            result = ProductRepository.create_product(request.data)
            if isinstance(result, dict):
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
            return Response(result.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        try:
            product = ProductRepository.get_product_by_id(pk)
            if not product:
                return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

            result = ProductRepository.update_product(product, request.data)
            if isinstance(result, dict) and 'error' in result:
                return Response(result, status=status.HTTP_400_BAD_REQUEST)

            return Response(ProductSerializer(result).data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update_inventory(self, request, pk=None):
        try:
            product = ProductRepository.get_product_by_id(pk)
            if not product:
                return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

            quantity = request.data.get('quantity')
            if quantity is None:
                return Response({"error": "Quantity is required to update inventory."}, status=status.HTTP_400_BAD_REQUEST)

            result = ProductRepository.update_inventory(pk, quantity)
            if isinstance(result, dict) and 'error' in result:
                return Response(result, status=status.HTTP_400_BAD_REQUEST)

            return Response(ProductSerializer(result).data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        try:
            page = request.query_params.get('page', 1)
            per_page = request.query_params.get('per_page', 10)

            
            low_stock = ProductRepository.check_low_stock_products(page=page, per_page=per_page)
            serializer = ProductSerializer(low_stock["products"], many=True)

            return Response({
                "low_stock_products": serializer.data,
                "total_low_stock_products": low_stock["total_products"],
                "total_pages": low_stock["total_pages"],
                "current_page": low_stock["current_page"],
            })
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UploadFileViewSet(viewsets.ViewSet):
    parser_classes = [MultiPartParser]

    def list(self, request):
        try:
            products = ProductRepository.get_all_products()
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, *args, **kwargs):
     
        file = request.FILES.get('file')
        if not file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        task = process_csv_task(file)

        return Response({
            "message": "CSV is being processed.",
            "task": task
        })
       
