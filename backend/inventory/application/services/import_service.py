from typing import List, Optional
from ...domain.interfaces.repository_interface import IRepository
from ...domain.models.imports import Import, ImportItem
from ..dto.import_dto import ImportDTO
from ...infrastructure.services.cache_service import CacheService
from ...infrastructure.repositories.import_repository import ImportRepository

class ImportService:
    """Application service for handling import-related operations."""
    
    def __init__(self, repository: ImportRepository, cache_service: CacheService):
        self.repository = repository
        self.cache_service = cache_service
    
    def get_import(self, import_id: int) -> Optional[ImportDTO]:
        """Get an import by ID with all its items."""
        import_obj = self.repository.get_with_items(import_id)
        return ImportDTO.from_entity(import_obj) if import_obj else None
    
    def get_recent_imports(self, limit: int = 10) -> List[ImportDTO]:
        """Get recent imports."""
        imports = self.repository.get_recent_imports(limit)
        return [ImportDTO.from_entity(import_obj) for import_obj in imports]
    
    def create_import(self, import_dto: ImportDTO) -> ImportDTO:
        """Create a new import."""
        import_obj = Import(
            status=import_dto.status,
            notes=import_dto.notes,
            created_by_id=import_dto.created_by_id
        )
        created_import = self.repository.create(import_obj)
        
        # Create import items
        for item in import_dto.items:
            ImportItem.objects.create(
                import_file=created_import,
                product_id=item.product_id,
                quantity=item.quantity,
                cost=item.cost
            )
        
        return self.get_import(created_import.id)
    
    def update_import_status(self, import_id: int, new_status: str) -> Optional[ImportDTO]:
        """Update the status of an import."""
        import_obj = self.repository.get_by_id(import_id)
        if not import_obj:
            return None
            
        import_obj.status = new_status
        updated_import = self.repository.update(import_obj)
        return ImportDTO.from_entity(updated_import)
    
    def delete_import(self, import_id: int) -> bool:
        """Delete an import and all its items."""
        return self.repository.delete(import_id)
