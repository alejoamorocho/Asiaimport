from typing import List, Dict, Any
from datetime import datetime, timedelta
from django.db.models import Sum, Avg, Count, F
from django.db.models.functions import TruncDate
from ..dto.product_dto import ProductDTO
from ...infrastructure.repositories.product_repository import ProductRepository
from ...infrastructure.repositories.import_repository import ImportRepository
from ...infrastructure.services.cache_service import CacheService

class ReportService:
    """Service for generating system reports."""
    
    def __init__(
        self,
        product_repository: ProductRepository,
        import_repository: ImportRepository,
        cache_service: CacheService
    ):
        self.product_repository = product_repository
        self.import_repository = import_repository
        self.cache_service = cache_service
    
    def get_low_stock_report(self, threshold: int = None) -> List[Dict[str, Any]]:
        """Generate report of products with low stock."""
        cache_key = f"low_stock_report:{threshold}"
        cached_report = self.cache_service.get(cache_key)
        
        if cached_report is not None:
            return cached_report
            
        products = self.product_repository.get_low_stock_products(threshold)
        report = [
            {
                'id': product.id,
                'name': product.name,
                'sku': product.sku,
                'current_stock': product.stock,
                'threshold': product.stock_threshold,
                'category': product.category.name if product.category else None
            }
            for product in products
        ]
        
        self.cache_service.set(cache_key, report, timeout=3600)  # Cache for 1 hour
        return report
    
    def get_import_summary_report(
        self,
        start_date: datetime,
        end_date: datetime
    ) -> Dict[str, Any]:
        """Generate summary report of imports within a date range."""
        cache_key = f"import_summary:{start_date.date()}:{end_date.date()}"
        cached_report = self.cache_service.get(cache_key)
        
        if cached_report is not None:
            return cached_report
            
        imports = self.import_repository.model_class.objects.filter(
            created_at__range=(start_date, end_date)
        )
        
        report = {
            'total_imports': imports.count(),
            'status_breakdown': imports.values('status').annotate(
                count=Count('id')
            ),
            'daily_imports': imports.annotate(
                date=TruncDate('created_at')
            ).values('date').annotate(
                count=Count('id')
            ).order_by('date'),
            'total_items': imports.aggregate(
                total=Sum('items__quantity')
            )['total'] or 0,
            'average_items_per_import': imports.annotate(
                items_count=Sum('items__quantity')
            ).aggregate(
                avg=Avg('items_count')
            )['avg'] or 0
        }
        
        self.cache_service.set(cache_key, report, timeout=3600)  # Cache for 1 hour
        return report
    
    def get_product_movement_report(
        self,
        product_id: int,
        days: int = 30
    ) -> Dict[str, Any]:
        """Generate report of product movement history."""
        cache_key = f"product_movement:{product_id}:{days}"
        cached_report = self.cache_service.get(cache_key)
        
        if cached_report is not None:
            return cached_report
            
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        product = self.product_repository.get_by_id(product_id)
        if not product:
            return None
            
        imports = product.import_items.filter(
            import_file__created_at__range=(start_date, end_date)
        ).select_related('import_file')
        
        report = {
            'product': ProductDTO.from_entity(product).to_dict(),
            'total_imported': imports.aggregate(
                total=Sum('quantity')
            )['total'] or 0,
            'daily_imports': imports.annotate(
                date=TruncDate('import_file__created_at')
            ).values('date').annotate(
                quantity=Sum('quantity'),
                cost=Avg('cost')
            ).order_by('date'),
            'average_cost': imports.aggregate(
                avg_cost=Avg('cost')
            )['avg_cost'] or 0
        }
        
        self.cache_service.set(cache_key, report, timeout=3600)  # Cache for 1 hour
        return report
    
    def get_category_performance_report(self) -> List[Dict[str, Any]]:
        """Generate report of category performance."""
        cache_key = "category_performance"
        cached_report = self.cache_service.get(cache_key)
        
        if cached_report is not None:
            return cached_report
            
        categories = self.product_repository.model_class.objects.values(
            'category__name'
        ).annotate(
            total_products=Count('id'),
            total_stock=Sum('stock'),
            average_price=Avg('price'),
            low_stock_products=Count(
                'id',
                filter=F('stock') <= F('stock_threshold')
            )
        ).exclude(category__isnull=True)
        
        report = list(categories)
        self.cache_service.set(cache_key, report, timeout=3600)  # Cache for 1 hour
        return report
