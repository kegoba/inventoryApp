from django.urls import path, include
from rest_framework.routers import DefaultRouter
from products.product.views import ProductViewSet  
from products.product.views import custom_404  
from products.product.views import UploadFileViewSet  
from products.supplier.views import SupplierViewSet
from products.inventory.views import InventoryViewSet, ReportViewSet

router = DefaultRouter()


handler404 = custom_404
router.register(r'products', ProductViewSet, basename='products') 
router.register(r'csv_upload', UploadFileViewSet, basename='csv_upload') 
router.register(r'suppliers', SupplierViewSet, basename='suppliers')  
router.register(r'inventory', InventoryViewSet, basename='inventory')  
router.register(r'report', ReportViewSet, basename='report') 

urlpatterns = [
    path('', include(router.urls)),
]
