from rest_framework import serializers
from ...domain.models.product import Product, Category
from ...domain.models import ProductUnit


class ProductSerializer(serializers.ModelSerializer):
    """Serializer básico para productos."""
    category_name = serializers.CharField(source='category.name', read_only=True)
    stock_status = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            'price',
            'category',
            'category_name',
            'stock',
            'min_stock',
            'sku',
            'barcode',
            'stock_status',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'sku', 'created_at', 'updated_at']

    def get_stock_status(self, obj):
        """Calcula el estado del stock."""
        if not hasattr(obj, '_stock_status'):
            if obj.stock <= 0:
                obj._stock_status = 'out_of_stock'
            elif obj.stock <= obj.min_stock:
                obj._stock_status = 'low_stock'
            else:
                obj._stock_status = 'in_stock'
        return obj._stock_status


class ProductDetailSerializer(ProductSerializer):
    """Serializer detallado para productos."""
    import_history = serializers.SerializerMethodField()
    category_details = serializers.SerializerMethodField()

    class Meta(ProductSerializer.Meta):
        fields = ProductSerializer.Meta.fields + [
            'import_history',
            'category_details'
        ]

    def get_import_history(self, obj):
        """
        Obtiene el historial de importaciones del producto.
        Usa prefetch_related para optimizar las consultas.
        """
        return [{
            'id': item.import_file.id,
            'date': item.import_file.created_at,
            'status': item.status,
            'raw_data': item.raw_data
        } for item in obj.import_items.all()[:5]]  # Limitar a las últimas 5

    def get_category_details(self, obj):
        """
        Obtiene detalles adicionales de la categoría.
        Usa select_related para optimizar las consultas.
        """
        category = obj.category
        if not category:
            return None
            
        return {
            'id': category.id,
            'name': category.name,
            'description': category.description,
            'is_active': category.is_active,
            'product_count': category.products.count()
        }

    def to_representation(self, instance):
        """
        Optimiza la representación del objeto.
        """
        # Cachear cálculos costosos
        if not hasattr(instance, '_cached_import_history'):
            instance._cached_import_history = self.get_import_history(instance)
        
        if not hasattr(instance, '_cached_category_details'):
            instance._cached_category_details = self.get_category_details(instance)

        # Obtener la representación base
        representation = super().to_representation(instance)
        
        # Agregar datos cacheados
        representation['import_history'] = instance._cached_import_history
        representation['category_details'] = instance._cached_category_details

        return representation


class ProductUnitSerializer(serializers.ModelSerializer):
    """
    Serializer for ProductUnit model.
    """
    class Meta:
        model = ProductUnit
        fields = ['id', 'product', 'serial_number', 'status', 'technical_sheet', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at', 'technical_sheet']
