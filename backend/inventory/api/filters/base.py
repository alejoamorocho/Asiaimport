import django_filters
from .models import Product, Import, ProductUnit

class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    category = django_filters.NumberFilter()
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = Product
        fields = ['name', 'category']

class ImportFilter(django_filters.FilterSet):
    reference_number = django_filters.CharFilter(lookup_expr='icontains')
    status = django_filters.ChoiceFilter(choices=Import.STATUS_CHOICES)
    import_date_after = django_filters.DateFilter(field_name='import_date', lookup_expr='gte')
    import_date_before = django_filters.DateFilter(field_name='import_date', lookup_expr='lte')

    class Meta:
        model = Import
        fields = ['reference_number', 'status', 'created_by']

class ProductUnitFilter(django_filters.FilterSet):
    serial_number = django_filters.CharFilter(lookup_expr='icontains')
    status = django_filters.ChoiceFilter(choices=ProductUnit.STATUS_CHOICES)
    product = django_filters.NumberFilter()
    import_item__import_record = django_filters.NumberFilter()

    class Meta:
        model = ProductUnit
        fields = ['serial_number', 'status', 'product', 'import_item__import_record']
