from dataclasses import dataclass
from typing import Optional
from decimal import Decimal

@dataclass
class ProductDTO:
    """Data Transfer Object for Product entities."""
    id: Optional[int]
    name: str
    description: Optional[str]
    sku: str
    barcode: Optional[str]
    price: Decimal
    stock: int
    category_id: Optional[int]
    
    @classmethod
    def from_entity(cls, entity) -> 'ProductDTO':
        """Create a DTO from a domain entity."""
        return cls(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            sku=entity.sku,
            barcode=entity.barcode,
            price=entity.price,
            stock=entity.stock,
            category_id=entity.category_id if entity.category else None
        )
    
    def to_dict(self) -> dict:
        """Convert DTO to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'sku': self.sku,
            'barcode': self.barcode,
            'price': str(self.price),
            'stock': self.stock,
            'category_id': self.category_id
        }
