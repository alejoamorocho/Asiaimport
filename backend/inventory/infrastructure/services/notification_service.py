from typing import List, Dict, Any
from django.core.mail import send_mail
from django.conf import settings
from ..services.event_service import EventService

class NotificationService:
    """Service for handling system notifications."""
    
    def __init__(self, event_service: EventService):
        self.event_service = event_service
        self._register_event_handlers()
    
    def _register_event_handlers(self) -> None:
        """Register handlers for system events."""
        self.event_service.subscribe('product_stock_low', self.handle_low_stock)
        self.event_service.subscribe('import_status_changed', self.handle_import_status_change)
    
    def send_email_notification(
        self,
        subject: str,
        message: str,
        recipients: List[str]
    ) -> bool:
        """Send email notification."""
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                recipients,
                fail_silently=False,
            )
            return True
        except Exception as e:
            print(f"Failed to send email: {str(e)}")
            return False
    
    def send_slack_notification(self, message: str, channel: str) -> bool:
        """Send Slack notification."""
        # Implementation would depend on your Slack integration
        # This is a placeholder
        try:
            print(f"Slack notification to {channel}: {message}")
            return True
        except Exception as e:
            print(f"Failed to send Slack notification: {str(e)}")
            return False
    
    def handle_low_stock(self, product: Any) -> None:
        """Handle low stock notification."""
        subject = f"Low Stock Alert: {product.name}"
        message = (
            f"Product {product.name} (SKU: {product.sku}) is running low on stock.\n"
            f"Current stock: {product.stock}\n"
            f"Threshold: {product.stock_threshold}"
        )
        
        # Send email to inventory managers
        self.send_email_notification(
            subject,
            message,
            settings.INVENTORY_MANAGER_EMAILS
        )
        
        # Send Slack notification
        self.send_slack_notification(
            message,
            "#inventory-alerts"
        )
    
    def handle_import_status_change(self, import_obj: Any) -> None:
        """Handle import status change notification."""
        subject = f"Import Status Update: #{import_obj.id}"
        message = (
            f"Import #{import_obj.id} status has been updated to {import_obj.status}.\n"
            f"Created by: {import_obj.created_by.username}\n"
            f"Notes: {import_obj.notes or 'No notes provided'}"
        )
        
        # Send email to relevant users
        recipients = [import_obj.created_by.email]
        if import_obj.status == 'completed':
            recipients.extend(settings.INVENTORY_MANAGER_EMAILS)
        
        self.send_email_notification(
            subject,
            message,
            recipients
        )
        
        # Send Slack notification for certain statuses
        if import_obj.status in ['completed', 'failed']:
            self.send_slack_notification(
                message,
                "#inventory-imports"
            )
