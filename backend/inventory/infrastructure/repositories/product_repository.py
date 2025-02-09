from typing import List, Optional
from django.db.models import Q, Prefetch
from ...domain.models.product import Product
from .base_repository import BaseRepository
from ..services.cache_service import CacheService

class ProductRepository(BaseRepository[Product]):
    """Repository implementation for Product entities."""
    
    def __init__(self, cache_service: CacheService):
        super().__init__(Product, cache_service)
    
    def search_products(self, query: str) -> List[Product]:
        """Search products by name, description, SKU or barcode."""
        cache_key = f"product_search:{query}"
        cached_results = self.cache_service.get(cache_key)
        
        if cached_results is not None:
            return cached_results
            
        results = self.model_class.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(sku__icontains=query) |
            Q(barcode__icontains=query)
        ).select_related('category')
        
        self.cache_service.set(cache_key, list(results))
        return results
    
    def get_by_category(self, category_id: int) -> List[Product]:
        """Get all products in a specific category."""
        cache_key = f"products_by_category:{category_id}"
        cached_results = self.cache_service.get(cache_key)
        
        if cached_results is not None:
            return cached_results
            
        results = self.model_class.objects.filter(
            category_id=category_id
        ).select_related('category')
        
        self.cache_service.set(cache_key, list(results))
        return results
    
    def get_low_stock_products(self, threshold: int = 10) -> List[Product]:
        """Get products with stock below threshold."""
        cache_key = f"low_stock_products:{threshold}"
        cached_results = self.cache_service.get(cache_key)
        
        if cached_results is not None:
            return cached_results
            
        results = self.model_class.objects.filter(
            stock__lte=threshold
        ).select_related('category')
        
        self.cache_service.set(cache_key, list(results))
        return results
    
    def get_by_sku(self, sku: str) -> Optional[Product]:
        """Get a product by its SKU."""
        cache_key = f"product_sku:{sku}"
        cached_result = self.cache_service.get(cache_key)
        
        if cached_result is not None:
            return cached_result
            
        product = self.model_class.objects.filter(sku=sku).first()
        
        if product:
            self.cache_service.set(cache_key, product)
        return product
