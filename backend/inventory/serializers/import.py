from rest_framework import serializers
from ..models.import import Import, ImportItem


class ImportItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportItem
        fields = [
            'id',
            'row_number',
            'status',
            'error_message',
            'product',
            'raw_data',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ImportSerializer(serializers.ModelSerializer):
    items = ImportItemSerializer(many=True, read_only=True)
    created_by = serializers.StringRelatedField(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    progress = serializers.SerializerMethodField()

    class Meta:
        model = Import
        fields = [
            'id',
            'file',
            'status',
            'status_display',
            'processed_rows',
            'total_rows',
            'error_log',
            'progress',
            'items',
            'created_by',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'id',
            'status',
            'processed_rows',
            'total_rows',
            'error_log',
            'created_by',
            'created_at',
            'updated_at'
        ]

    def get_progress(self, obj):
        """Calcula el progreso de la importación en porcentaje."""
        if obj.total_rows == 0:
            return 0
        return round((obj.processed_rows / obj.total_rows) * 100, 2)

    def validate_file(self, value):
        """Valida el archivo de importación."""
        if not value.name.endswith(('.xlsx', '.xls', '.csv')):
            raise serializers.ValidationError(
                "El archivo debe ser de tipo Excel (.xlsx, .xls) o CSV (.csv)"
            )
        
        # Validar tamaño máximo (10MB)
        if value.size > 10 * 1024 * 1024:
            raise serializers.ValidationError(
                "El archivo no puede ser mayor a 10MB"
            )
        
        return value
