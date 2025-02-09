"""
ViewSet for ImportItem model.
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ...domain.models import ImportItem
from ..serializers.imports import ImportItemSerializer


class ImportItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing import items.
    """
    queryset = ImportItem.objects.all()
    serializer_class = ImportItemSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['status', 'import_record']
    search_fields = ['product__name', 'error_message']
    ordering_fields = ['created_at', 'row_number']
