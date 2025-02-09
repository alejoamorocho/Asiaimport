"""
ViewSet for ProductUnit model.
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ...domain.models import ProductUnit
from ..serializers.product import ProductUnitSerializer


class ProductUnitViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing product units.
    """
    queryset = ProductUnit.objects.all()
    serializer_class = ProductUnitSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['status', 'product']
    search_fields = ['serial_number', 'product__name']
    ordering_fields = ['created_at', 'serial_number']
