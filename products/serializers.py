from rest_framework import serializers
from .models import Product
from suppliers.models import Supplier

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'supplier_id']

    def validate_name(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Product not valid.")
        return value

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price not valid")
        return value
    def validate_description(self, value):
        if len(value.strip()) <= 3:
            raise serializers.ValidationError("Description not valid")
        return value

    def validate(self, data):
        if data['name'].lower() in data['description'].lower():
            raise serializers.ValidationError("invalid data")
        return data
