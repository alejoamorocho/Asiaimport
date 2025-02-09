from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ValidationError
from ...application.services.product_service import ProductService
from ...application.dto.product_dto import ProductDTO
from ..serializers.product import ProductSerializer
from ...infrastructure.repositories.base_repository import BaseRepository
from ...infrastructure.services.cache_service import CacheService
from ...domain.models.product import Product

class ProductViewSet(viewsets.ViewSet):
    """API endpoint for managing products using clean architecture."""
    
    permission_classes = [IsAuthenticated]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        cache_service = CacheService()
        repository = BaseRepository[Product](Product, cache_service)
        self.product_service = ProductService(repository, cache_service)
    
    def list(self, request):
        """Get all products."""
        products = self.product_service.get_all_products()
        serializer = ProductSerializer(
            [product.to_dict() for product in products], 
            many=True
        )
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        """Get a specific product."""
        try:
            product = self.product_service.get_product(int(pk))
            if not product:
                return Response(
                    {'detail': 'Product not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = ProductSerializer(product.to_dict())
            return Response(serializer.data)
        except ValueError:
            return Response(
                {'detail': 'Invalid product ID'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def create(self, request):
        """Create a new product."""
        serializer = ProductSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            product_dto = ProductDTO(**serializer.validated_data)
            created_product = self.product_service.create_product(product_dto)
            return Response(
                ProductSerializer(created_product.to_dict()).data, 
                status=status.HTTP_201_CREATED
            )
        except ValidationError as e:
            return Response(
                {'detail': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def update(self, request, pk=None):
        """Update an existing product."""
        try:
            existing_product = self.product_service.get_product(int(pk))
            if not existing_product:
                return Response(
                    {'detail': 'Product not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
                
            serializer = ProductSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    serializer.errors, 
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            product_dto = ProductDTO(id=int(pk), **serializer.validated_data)
            updated_product = self.product_service.update_product(product_dto)
            
            return Response(ProductSerializer(updated_product.to_dict()).data)
        except ValueError:
            return Response(
                {'detail': 'Invalid product ID'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def destroy(self, request, pk=None):
        """Delete a product."""
        try:
            if self.product_service.delete_product(int(pk)):
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                {'detail': 'Product not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except ValueError:
            return Response(
                {'detail': 'Invalid product ID'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
