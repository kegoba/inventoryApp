
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import ProductSerializer
from .repositories import ProductRepository

class ProductViewSet(viewsets.ViewSet):

    def list(self, request):
        products = ProductRepository.get_all_products()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        product = ProductRepository.get_product_by_id(pk)
        if not product:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def create(self, request):
        # Call the repository to create a new product and handle potential errors
        result = ProductRepository.create_product(request.data)
        if isinstance(result, dict) and 'error' in result:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        return Response(result.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        product = ProductRepository.get_product_by_id(pk)
        if not product:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        # Delegate to repository for update
        result = ProductRepository.update_product(product, request.data)
        if isinstance(result, dict) and 'error' in result:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

        return Response(ProductSerializer(result).data)

    def update_inventory(self, request, pk=None):
        product = ProductRepository.get_product_by_id(pk)
        if not product:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        # Ensure 'quantity' is provided
        quantity = request.data.get('quantity')
        if quantity is None:
            return Response({"error": "Quantity is required to update inventory."}, status=status.HTTP_400_BAD_REQUEST)

        # Delegate to repository for inventory update
        result = ProductRepository.update_inventory(pk, quantity)
        if isinstance(result, dict) and 'error' in result:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

        return Response(ProductSerializer(result).data)

    @action(detail=False, methods=['get'])
    def low_stock_alert(self, request):
        # Call repository to fetch low stock products
        low_stock_products = ProductRepository.check_low_stock_products()
        serializer = ProductSerializer(low_stock_products, many=True)
        return Response(serializer.data)
