from typing import List, Optional
from ...domain.interfaces.repository_interface import IRepository
from ...domain.models.product import Product
from ..dto.product_dto import ProductDTO
from ...infrastructure.services.cache_service import CacheService

class ProductService:
    """Application service for handling product-related operations."""
    
    def __init__(self, repository: IRepository[Product], cache_service: CacheService):
        self.repository = repository
        self.cache_service = cache_service
    
    def get_product(self, product_id: int) -> Optional[ProductDTO]:
        """Get a product by ID."""
        product = self.repository.get_by_id(product_id)
        return ProductDTO.from_entity(product) if product else None
    
    def get_all_products(self) -> List[ProductDTO]:
        """Get all products."""
        products = self.repository.get_all()
        return [ProductDTO.from_entity(product) for product in products]
    
    def create_product(self, product_dto: ProductDTO) -> ProductDTO:
        """Create a new product."""
        product = Product(
            name=product_dto.name,
            description=product_dto.description,
            sku=product_dto.sku,
            barcode=product_dto.barcode,
            price=product_dto.price,
            stock=product_dto.stock,
            category_id=product_dto.category_id
        )
        created_product = self.repository.create(product)
        return ProductDTO.from_entity(created_product)
    
    def update_product(self, product_dto: ProductDTO) -> Optional[ProductDTO]:
        """Update an existing product."""
        if not product_dto.id:
            return None
            
        existing_product = self.repository.get_by_id(product_dto.id)
        if not existing_product:
            return None
            
        for field, value in product_dto.to_dict().items():
            if field != 'id' and hasattr(existing_product, field):
                setattr(existing_product, field, value)
                
        updated_product = self.repository.update(existing_product)
        return ProductDTO.from_entity(updated_product)
    
    def delete_product(self, product_id: int) -> bool:
        """Delete a product."""
        return self.repository.delete(product_id)
