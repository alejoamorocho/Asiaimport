from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Product, Import, ImportItem, ProductUnit
from .serializers import (
    CategorySerializer, ProductSerializer, ImportSerializer,
    ImportItemSerializer, ProductUnitSerializer, ImportDetailSerializer
)
# Temporarily commented out
# from .utils import generate_import_report, generate_product_technical_sheet

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category']
    search_fields = ['name', 'description']

    # Temporarily commented out
    # @action(detail=True, methods=['get'])
    # def technical_sheet(self, request, pk=None):
    #     product = self.get_object()
    #     pdf_file = generate_product_technical_sheet(product)
    #     response = HttpResponse(pdf_file, content_type='application/pdf')
    #     response['Content-Disposition'] = f'attachment; filename="{product.name}_technical_sheet.pdf"'
    #     return response

class ImportViewSet(viewsets.ModelViewSet):
    queryset = Import.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status']
    search_fields = ['reference_number', 'notes']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ImportDetailSerializer
        return ImportSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    # Temporarily commented out
    # @action(detail=True, methods=['get'])
    # def verification_report(self, request, pk=None):
    #     import_obj = self.get_object()
    #     pdf_file = generate_import_report(import_obj)
    #     response = HttpResponse(pdf_file, content_type='application/pdf')
    #     response['Content-Disposition'] = f'attachment; filename="import_{import_obj.reference_number}_report.pdf"'
    #     return response

    @action(detail=True, methods=['post'])
    def verify_items(self, request, pk=None):
        import_obj = self.get_object()
        items_data = request.data.get('items', [])
        
        for item_data in items_data:
            item = get_object_or_404(ImportItem, id=item_data['id'], import_record=import_obj)
            item.received_quantity = item_data.get('received_quantity', item.received_quantity)
            item.notes = item_data.get('notes', item.notes)
            item.save()
            
            # Create product units if provided
            units_data = item_data.get('units', [])
            for unit_data in units_data:
                ProductUnit.objects.create(
                    import_item=item,
                    product=item.product,
                    serial_number=unit_data['serial_number'],
                    status='available',
                    notes=unit_data.get('notes', '')
                )
        
        if all(item.expected_quantity == item.received_quantity for item in import_obj.items.all()):
            import_obj.status = 'completed'
        else:
            import_obj.status = 'in_progress'
        import_obj.save()
        
        return Response(ImportDetailSerializer(import_obj).data)

class ImportItemViewSet(viewsets.ModelViewSet):
    queryset = ImportItem.objects.all()
    serializer_class = ImportItemSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['import_record', 'product']

class ProductUnitViewSet(viewsets.ModelViewSet):
    queryset = ProductUnit.objects.all()
    serializer_class = ProductUnitSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', 'product', 'import_item']
    search_fields = ['serial_number', 'notes']
