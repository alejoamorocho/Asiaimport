from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, Product, Import, ImportItem, ProductUnit

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Product
        fields = ('id', 'name', 'category', 'category_name', 'description', 
                 'specifications', 'created_at', 'updated_at')

class ProductUnitSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    
    class Meta:
        model = ProductUnit
        fields = ('id', 'product', 'product_name', 'import_item', 'serial_number', 
                 'status', 'notes', 'created_at', 'updated_at')

class ImportItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    units = ProductUnitSerializer(many=True, read_only=True)
    
    class Meta:
        model = ImportItem
        fields = ('id', 'import_record', 'product', 'product_name', 
                 'expected_quantity', 'received_quantity', 'notes', 
                 'units', 'created_at', 'updated_at')

class ImportSerializer(serializers.ModelSerializer):
    items = ImportItemSerializer(many=True, read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = Import
        fields = ('id', 'reference_number', 'status', 'import_date', 
                 'created_by', 'created_by_username', 'documents', 
                 'notes', 'items', 'created_at', 'updated_at')
        read_only_fields = ('created_by',)

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

class ImportDetailSerializer(ImportSerializer):
    """Serializer for detailed import view with all nested relationships"""
    items = serializers.SerializerMethodField()

    def get_items(self, obj):
        items = obj.items.all()
        return ImportItemDetailSerializer(items, many=True).data

class ImportItemDetailSerializer(ImportItemSerializer):
    """Detailed serializer for import items including all units"""
    units = ProductUnitSerializer(many=True)
    
    def create(self, validated_data):
        units_data = validated_data.pop('units', [])
        import_item = ImportItem.objects.create(**validated_data)
        
        for unit_data in units_data:
            ProductUnit.objects.create(import_item=import_item, **unit_data)
        
        return import_item
