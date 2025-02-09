from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional

T = TypeVar('T')

class IRepository(Generic[T], ABC):
    """Base repository interface following the Repository pattern."""
    
    @abstractmethod
    def get_by_id(self, id: int) -> Optional[T]:
        """Retrieve an entity by its ID."""
        pass
    
    @abstractmethod
    def get_all(self) -> List[T]:
        """Retrieve all entities."""
        pass
    
    @abstractmethod
    def create(self, entity: T) -> T:
        """Create a new entity."""
        pass
    
    @abstractmethod
    def update(self, entity: T) -> T:
        """Update an existing entity."""
        pass
    
    @abstractmethod
    def delete(self, id: int) -> bool:
        """Delete an entity by its ID."""
        pass
