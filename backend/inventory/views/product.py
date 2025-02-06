from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, Count, Prefetch, F
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from ..models.product import Product
from ..serializers.product import ProductSerializer, ProductDetailSerializer
from ..filters.product import ProductFilter
from ..utils.cache import cache_response, clear_model_cache
from ..permissions import IsStaffOrReadOnly
from drf_spectacular.utils import extend_schema, OpenApiParameter


@extend_schema(tags=['Products'])
class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar productos.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsStaffOrReadOnly]
    filterset_class = ProductFilter
    search_fields = ['name', 'description', 'sku', 'barcode']
    ordering_fields = ['name', 'price', 'stock', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        """
        Optimiza las consultas usando select_related y prefetch_related.
        """
        queryset = super().get_queryset()
        if self.action in ['list', 'retrieve']:
            queryset = queryset.select_related('category')
            
            # Si se solicitan detalles completos
            if self.action == 'retrieve':
                queryset = queryset.prefetch_related(
                    'import_items',
                    Prefetch(
                        'import_items__import_file',
                        queryset=Import.objects.only('id', 'created_at')
                    )
                )
        
        return queryset

    def get_serializer_class(self):
        """
        Usa un serializer diferente para detalles.
        """
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return super().get_serializer_class()

    @cache_response(timeout=60*5, key_prefix='product')
    def list(self, request, *args, **kwargs):
        """
        Lista productos con caché de 5 minutos.
        """
        return super().list(request, *args, **kwargs)

    @cache_response(timeout=60*15, key_prefix='product')
    def retrieve(self, request, *args, **kwargs):
        """
        Obtiene detalles de un producto con caché de 15 minutos.
        """
        return super().retrieve(request, *args, **kwargs)

    def perform_create(self, serializer):
        """
        Crea un producto y limpia el caché relacionado.
        """
        product = serializer.save()
        clear_model_cache('product')

    def perform_update(self, serializer):
        """
        Actualiza un producto y limpia el caché relacionado.
        """
        product = serializer.save()
        clear_model_cache('product')

    def perform_destroy(self, instance):
        """
        Elimina un producto y limpia el caché relacionado.
        """
        instance.delete()
        clear_model_cache('product')

    @action(detail=False, methods=['get'])
    @cache_response(timeout=60*30, key_prefix='product')
    def low_stock(self, request):
        """
        Lista productos con stock bajo.
        """
        products = self.get_queryset().filter(
            Q(stock__lte=F('min_stock')) |
            Q(stock=0)
        )
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def adjust_stock(self, request, pk=None):
        """
        Ajusta el stock de un producto y limpia el caché.
        """
        product = self.get_object()
        try:
            quantity = int(request.data.get('quantity', 0))
            product.stock += quantity
            product.save()
            clear_model_cache('product')
            return Response({
                'message': 'Stock ajustado correctamente',
                'new_stock': product.stock
            })
        except ValueError:
            return Response(
                {'error': 'Cantidad inválida'},
                status=status.HTTP_400_BAD_REQUEST
            )
