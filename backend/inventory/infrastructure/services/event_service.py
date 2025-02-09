from typing import Any, Dict, List, Callable
from django.dispatch import Signal, receiver
from django.db.models.signals import post_save, post_delete
from ...domain.models.product import Product
from ...domain.models.imports import Import

class EventService:
    """Service for handling system events and notifications."""
    
    # Custom signals
    product_stock_low = Signal()  # Sent when product stock is below threshold
    import_status_changed = Signal()  # Sent when import status changes
    
    def __init__(self):
        self._event_handlers: Dict[str, List[Callable]] = {
            'product_stock_low': [],
            'import_status_changed': [],
            'product_created': [],
            'product_updated': [],
            'product_deleted': [],
            'import_created': [],
            'import_updated': [],
            'import_deleted': []
        }
        
        # Register model signals
        self._register_model_signals()
    
    def subscribe(self, event_type: str, handler: Callable) -> None:
        """Subscribe to an event type."""
        if event_type in self._event_handlers:
            self._event_handlers[event_type].append(handler)
    
    def unsubscribe(self, event_type: str, handler: Callable) -> None:
        """Unsubscribe from an event type."""
        if event_type in self._event_handlers:
            self._event_handlers[event_type].remove(handler)
    
    def notify(self, event_type: str, data: Any) -> None:
        """Notify all subscribers of an event."""
        if event_type in self._event_handlers:
            for handler in self._event_handlers[event_type]:
                handler(data)
    
    def _register_model_signals(self) -> None:
        """Register Django model signals."""
        
        @receiver(post_save, sender=Product)
        def handle_product_save(sender, instance, created, **kwargs):
            event_type = 'product_created' if created else 'product_updated'
            self.notify(event_type, instance)
            
            # Check for low stock
            if instance.stock <= instance.stock_threshold:
                self.notify('product_stock_low', instance)
        
        @receiver(post_delete, sender=Product)
        def handle_product_delete(sender, instance, **kwargs):
            self.notify('product_deleted', instance)
        
        @receiver(post_save, sender=Import)
        def handle_import_save(sender, instance, created, **kwargs):
            event_type = 'import_created' if created else 'import_updated'
            self.notify(event_type, instance)
            
            # Check for status changes
            if not created and instance.tracker.has_changed('status'):
                self.notify('import_status_changed', instance)
        
        @receiver(post_delete, sender=Import)
        def handle_import_delete(sender, instance, **kwargs):
            self.notify('import_deleted', instance)
    
    # Example event handlers
    @staticmethod
    def handle_low_stock(product: Product) -> None:
        """Handle low stock notification."""
        print(f"Low stock alert for product {product.name} (SKU: {product.sku})")
        # Here you could send emails, Slack notifications, etc.
    
    @staticmethod
    def handle_import_status_change(import_obj: Import) -> None:
        """Handle import status change notification."""
        print(f"Import {import_obj.id} status changed to {import_obj.status}")
        # Here you could send notifications, update external systems, etc.
