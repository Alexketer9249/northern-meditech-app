from rest_framework import serializers
from .models import Category, Product, RFQSubmission

# 1. Serializer for Categories (This was missing!)
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

# 2. Serializer for Products
class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'model_number', 'category_name', 'description', 'image', 'is_available']

# 3. Serializer for RFQs
class RFQSerializer(serializers.ModelSerializer):
    class Meta:
        model = RFQSubmission
        fields = '__all__'