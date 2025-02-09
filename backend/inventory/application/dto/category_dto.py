from dataclasses import dataclass
from typing import Optional, List

@dataclass
class CategoryDTO:
    """Data Transfer Object for Category entities."""
    id: Optional[int]
    name: str
    description: Optional[str]
    parent_id: Optional[int]
    slug: str
    
    @classmethod
    def from_entity(cls, entity) -> 'CategoryDTO':
        """Create a DTO from a domain entity."""
        return cls(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            parent_id=entity.parent_id if entity.parent else None,
            slug=entity.slug
        )
    
    def to_dict(self) -> dict:
        """Convert DTO to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'parent_id': self.parent_id,
            'slug': self.slug
        }
