from dataclasses import dataclass
from typing import Optional, List
from decimal import Decimal
from datetime import datetime

@dataclass
class ImportItemDTO:
    """Data Transfer Object for Import Item entities."""
    id: Optional[int]
    import_id: Optional[int]
    product_id: int
    quantity: int
    cost: Decimal
    
    @classmethod
    def from_entity(cls, entity) -> 'ImportItemDTO':
        """Create a DTO from a domain entity."""
        return cls(
            id=entity.id,
            import_id=entity.import_file_id,
            product_id=entity.product_id,
            quantity=entity.quantity,
            cost=entity.cost
        )

@dataclass
class ImportDTO:
    """Data Transfer Object for Import entities."""
    id: Optional[int]
    status: str
    notes: Optional[str]
    created_by_id: int
    created_at: Optional[datetime]
    items: List[ImportItemDTO]
    
    @classmethod
    def from_entity(cls, entity) -> 'ImportDTO':
        """Create a DTO from a domain entity."""
        return cls(
            id=entity.id,
            status=entity.status,
            notes=entity.notes,
            created_by_id=entity.created_by_id,
            created_at=entity.created_at,
            items=[ImportItemDTO.from_entity(item) for item in entity.items.all()]
        )
    
    def to_dict(self) -> dict:
        """Convert DTO to dictionary."""
        return {
            'id': self.id,
            'status': self.status,
            'notes': self.notes,
            'created_by_id': self.created_by_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'items': [
                {
                    'id': item.id,
                    'product_id': item.product_id,
                    'quantity': item.quantity,
                    'cost': str(item.cost)
                }
                for item in self.items
            ]
        }
