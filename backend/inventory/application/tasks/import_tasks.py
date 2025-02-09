from celery import shared_task
from django.conf import settings
from ...domain.models.imports import Import
from ...domain.models.product import Product
from ...infrastructure.services.notification_service import NotificationService
from ...infrastructure.services.event_service import EventService

@shared_task
def process_import(import_id: int) -> bool:
    """
    Process an import in the background.
    Updates product quantities and sends notifications.
    """
    try:
        import_obj = Import.objects.select_related('created_by').prefetch_related('items').get(id=import_id)
        import_obj.status = 'processing'
        import_obj.save()
        
        # Process each import item
        for item in import_obj.items.all():
            product = item.product
            product.stock += item.quantity
            product.save()
        
        import_obj.status = 'completed'
        import_obj.save()
        
        # Send notifications
        event_service = EventService()
        notification_service = NotificationService(event_service)
        notification_service.handle_import_status_change(import_obj)
        
        return True
    except Exception as e:
        if import_obj:
            import_obj.status = 'failed'
            import_obj.notes = f"Error processing import: {str(e)}"
            import_obj.save()
        return False

@shared_task
def check_low_stock() -> None:
    """
    Periodic task to check for low stock products and send notifications.
    """
    event_service = EventService()
    notification_service = NotificationService(event_service)
    
    low_stock_products = Product.objects.filter(
        stock__lte=F('stock_threshold')
    ).select_related('category')
    
    for product in low_stock_products:
        notification_service.handle_low_stock(product)

@shared_task
def generate_periodic_reports() -> None:
    """
    Periodic task to generate and cache system reports.
    """
    from ...application.services.report_service import ReportService
    from ...infrastructure.repositories.product_repository import ProductRepository
    from ...infrastructure.repositories.import_repository import ImportRepository
    from ...infrastructure.services.cache_service import CacheService
    
    cache_service = CacheService()
    product_repository = ProductRepository(cache_service)
    import_repository = ImportRepository(cache_service)
    report_service = ReportService(product_repository, import_repository, cache_service)
    
    # Generate and cache reports
    report_service.get_low_stock_report()
    report_service.get_category_performance_report()
    
    # Generate last 30 days import summary
    from datetime import datetime, timedelta
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    report_service.get_import_summary_report(start_date, end_date)
