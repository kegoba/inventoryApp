from rest_framework import serializers
from products.models import Product,Supplier


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'quantity' ,'description', 'price', 'supplier_id']

    def validate_name(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Product not valid.")
        return value

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price not valid")
        return value
    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("quantity not valid")
        return value
    def validate_description(self, value):
        if len(value.strip()) <= 3:
            raise serializers.ValidationError("Description not valid")
        return value

    # def validate(self, data):
    #     if data['name'].lower() in data['description'].lower():
    #         raise serializers.ValidationError("invalid description and name must not have sim")
    #     return data


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate_file(self, value):
        # Optional: Add any specific validation logic if needed
        return value