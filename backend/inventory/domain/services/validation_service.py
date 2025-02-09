from typing import List, Dict, Any
from django.core.exceptions import ValidationError
from ..models.product import Product
from ..models.imports import Import, ImportItem

class ValidationService:
    """Service for handling business rule validations."""
    
    @staticmethod
    def validate_product(data: Dict[str, Any]) -> List[str]:
        """Validate product data according to business rules."""
        errors = []
        
        # Required fields
        required_fields = ['name', 'sku', 'price']
        for field in required_fields:
            if not data.get(field):
                errors.append(f"{field} is required")
        
        # Price validation
        if data.get('price') and float(data['price']) <= 0:
            errors.append("Price must be greater than 0")
        
        # Stock validation
        if 'stock' in data and data['stock'] < 0:
            errors.append("Stock cannot be negative")
        
        # SKU format validation (example: assuming SKU should be alphanumeric)
        if data.get('sku') and not data['sku'].isalnum():
            errors.append("SKU must be alphanumeric")
        
        return errors
    
    @staticmethod
    def validate_import(data: Dict[str, Any]) -> List[str]:
        """Validate import data according to business rules."""
        errors = []
        
        # Required fields
        if not data.get('status'):
            errors.append("Status is required")
        
        # Status validation
        valid_statuses = ['pending', 'processing', 'completed', 'failed']
        if data.get('status') and data['status'] not in valid_statuses:
            errors.append(f"Status must be one of: {', '.join(valid_statuses)}")
        
        # Items validation
        items = data.get('items', [])
        if not items:
            errors.append("Import must have at least one item")
        
        for item in items:
            if not item.get('product_id'):
                errors.append("Each item must have a product_id")
            if not item.get('quantity') or item['quantity'] <= 0:
                errors.append("Each item must have a positive quantity")
            if not item.get('cost') or float(item['cost']) <= 0:
                errors.append("Each item must have a positive cost")
        
        return errors
    
    @staticmethod
    def validate_import_status_transition(current_status: str, new_status: str) -> List[str]:
        """Validate if a status transition is allowed."""
        errors = []
        
        # Define valid status transitions
        valid_transitions = {
            'pending': ['processing', 'failed'],
            'processing': ['completed', 'failed'],
            'completed': [],  # No transitions allowed from completed
            'failed': ['pending']  # Can retry failed imports
        }
        
        if current_status not in valid_transitions:
            errors.append(f"Invalid current status: {current_status}")
        elif new_status not in valid_transitions[current_status]:
            errors.append(
                f"Cannot transition from {current_status} to {new_status}. "
                f"Valid transitions are: {', '.join(valid_transitions[current_status])}"
            )
        
        return errors
