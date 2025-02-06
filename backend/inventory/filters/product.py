import django_filters
from ..models.product import Product


class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr='lte')
    min_stock = django_filters.NumberFilter(field_name="stock", lookup_expr='gte')
    max_stock = django_filters.NumberFilter(field_name="stock", lookup_expr='lte')
    category = django_filters.NumberFilter(field_name="category__id")
    needs_restock = django_filters.BooleanFilter(method='filter_needs_restock')
    created_after = django_filters.DateFilter(field_name="created_at", lookup_expr='gte')
    created_before = django_filters.DateFilter(field_name="created_at", lookup_expr='lte')
    is_active = django_filters.BooleanFilter()

    class Meta:
        model = Product
        fields = {
            'name': ['icontains'],
            'description': ['icontains'],
            'sku': ['exact', 'icontains'],
            'barcode': ['exact', 'icontains'],
        }

    def filter_needs_restock(self, queryset, name, value):
        if value:
            return queryset.filter(stock__lte=models.F('min_stock'))
        return queryset
