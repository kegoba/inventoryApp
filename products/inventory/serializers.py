from rest_framework import serializers
from products.models import Product,Supplier


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'quantity', 'price', 'supplier_id']


    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price not valid")
        return value
    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("quantity not valid")
        return value


