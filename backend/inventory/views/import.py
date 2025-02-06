from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from ..models.import import Import, ImportItem
from ..serializers.import import ImportSerializer, ImportItemSerializer
from ..tasks import process_import_file
from drf_spectacular.utils import extend_schema, OpenApiParameter


@extend_schema(tags=['Imports'])
class ImportViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar importaciones de productos.
    """
    queryset = Import.objects.all()
    serializer_class = ImportSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['status']
    search_fields = ['file', 'created_by__username']
    ordering_fields = ['created_at', 'status', 'processed_rows']
    ordering = ['-created_at']

    def get_queryset(self):
        """Filtra las importaciones según el usuario."""
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(created_by=self.request.user)
        return queryset.select_related('created_by')

    def perform_create(self, serializer):
        """Asigna el usuario actual como creador y inicia el procesamiento."""
        with transaction.atomic():
            import_obj = serializer.save(created_by=self.request.user)
            # Iniciar tarea asíncrona de procesamiento
            process_import_file.delay(import_obj.id)

    @action(detail=True, methods=['post'])
    def retry(self, request, pk=None):
        """
        Reintenta procesar una importación fallida.
        """
        import_obj = self.get_object()
        if import_obj.status != 'failed':
            return Response(
                {'error': 'Solo se pueden reintentar importaciones fallidas'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Reiniciar estado y contadores
        import_obj.status = 'pending'
        import_obj.processed_rows = 0
        import_obj.error_log = ''
        import_obj.save()

        # Eliminar items anteriores
        import_obj.items.all().delete()

        # Iniciar nuevo procesamiento
        process_import_file.delay(import_obj.id)

        return Response({'status': 'Procesamiento reiniciado'})

    @action(detail=True, methods=['get'])
    def items(self, request, pk=None):
        """
        Retorna los items de una importación con paginación.
        """
        import_obj = self.get_object()
        items = import_obj.items.all()

        # Aplicar filtros
        status_filter = request.query_params.get('status')
        if status_filter:
            items = items.filter(status=status_filter)

        page = self.paginate_queryset(items)
        if page is not None:
            serializer = ImportItemSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = ImportItemSerializer(items, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def download_template(self, request, pk=None):
        """
        Descarga una plantilla Excel para la importación de productos.
        """
        import pandas as pd
        from django.http import HttpResponse
        from io import BytesIO

        # Crear DataFrame con las columnas requeridas
        df = pd.DataFrame(columns=[
            'nombre',
            'descripcion',
            'precio',
            'categoria',
            'stock',
            'codigo_barras',
            'stock_minimo'
        ])

        # Crear archivo Excel en memoria
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='openpyxl')
        df.to_excel(writer, index=False)
        writer.save()
        output.seek(0)

        # Crear respuesta HTTP
        response = HttpResponse(
            output.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=plantilla_importacion.xlsx'
        
        return response
