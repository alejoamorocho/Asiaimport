from typing import List, Optional
from django.db.models import Prefetch
from ...domain.models.imports import Import, ImportItem
from .base_repository import BaseRepository
from ..services.cache_service import CacheService

class ImportRepository(BaseRepository[Import]):
    """Repository implementation for Import entities."""
    
    def __init__(self, cache_service: CacheService):
        super().__init__(Import, cache_service)
    
    def get_with_items(self, import_id: int) -> Optional[Import]:
        """Get an import with all its items."""
        cache_key = f"import_with_items:{import_id}"
        cached_result = self.cache_service.get(cache_key)
        
        if cached_result is not None:
            return cached_result
            
        import_obj = self.model_class.objects.filter(id=import_id).prefetch_related(
            Prefetch(
                'items',
                queryset=ImportItem.objects.select_related('product')
            )
        ).first()
        
        if import_obj:
            self.cache_service.set(cache_key, import_obj)
        return import_obj
    
    def get_recent_imports(self, limit: int = 10) -> List[Import]:
        """Get recent imports with their items."""
        cache_key = f"recent_imports:{limit}"
        cached_results = self.cache_service.get(cache_key)
        
        if cached_results is not None:
            return cached_results
            
        results = self.model_class.objects.order_by('-created_at')[:limit].prefetch_related(
            Prefetch(
                'items',
                queryset=ImportItem.objects.select_related('product')
            )
        )
        
        self.cache_service.set(cache_key, list(results))
        return results
    
    def get_by_status(self, status: str) -> List[Import]:
        """Get imports by their status."""
        cache_key = f"imports_by_status:{status}"
        cached_results = self.cache_service.get(cache_key)
        
        if cached_results is not None:
            return cached_results
            
        results = self.model_class.objects.filter(status=status).prefetch_related(
            Prefetch(
                'items',
                queryset=ImportItem.objects.select_related('product')
            )
        )
        
        self.cache_service.set(cache_key, list(results))
        return results
