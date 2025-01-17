from rest_framework import serializers
from products.models import Supplier

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'first_name','last_name', 'email']

    def validate_first_name(self, value):
       #name validation
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Invalid Supplier first name.")
        return value
    def validate_last_name(self, value):
       #name validation
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Invalid Supplier last name.")
        return value
    def validate_email(self, value):
        if Supplier.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        if "@" not in value:
            raise serializers.ValidationError("Invalid email info.")
        
        return value
