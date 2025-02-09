from typing import TypeVar, Generic, List, Optional, Type
from django.db import models
from ...domain.interfaces.repository_interface import IRepository
from ..services.cache_service import CacheService

T = TypeVar('T', bound=models.Model)

class BaseRepository(IRepository[T], Generic[T]):
    """Base implementation of the repository pattern for Django models."""
    
    def __init__(self, model_class: Type[T], cache_service: CacheService):
        self.model_class = model_class
        self.cache_service = cache_service
        self.cache_prefix = model_class.__name__.lower()
    
    def _get_cache_key(self, id: int) -> str:
        return f"{self.cache_prefix}:{id}"
    
    def get_by_id(self, id: int) -> Optional[T]:
        cache_key = self._get_cache_key(id)
        cached_item = self.cache_service.get(cache_key)
        
        if cached_item:
            return cached_item
            
        item = self.model_class.objects.filter(id=id).first()
        if item:
            self.cache_service.set(cache_key, item)
        return item
    
    def get_all(self) -> List[T]:
        return list(self.model_class.objects.all())
    
    def create(self, entity: T) -> T:
        entity.save()
        cache_key = self._get_cache_key(entity.id)
        self.cache_service.set(cache_key, entity)
        return entity
    
    def update(self, entity: T) -> T:
        entity.save()
        cache_key = self._get_cache_key(entity.id)
        self.cache_service.set(cache_key, entity)
        return entity
    
    def delete(self, id: int) -> bool:
        try:
            entity = self.get_by_id(id)
            if entity:
                entity.delete()
                cache_key = self._get_cache_key(id)
                self.cache_service.delete(cache_key)
                return True
            return False
        except Exception:
            return False
