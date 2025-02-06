from django.contrib import admin
from .models import Category, Product, Import, ImportItem, ProductUnit

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'created_at', 'updated_at')
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'description')

class ImportItemInline(admin.TabularInline):
    model = ImportItem
    extra = 1

class ProductUnitInline(admin.TabularInline):
    model = ProductUnit
    extra = 0

@admin.register(Import)
class ImportAdmin(admin.ModelAdmin):
    list_display = ('reference_number', 'status', 'import_date', 'created_by', 'created_at')
    list_filter = ('status', 'import_date', 'created_at')
    search_fields = ('reference_number', 'notes')
    inlines = [ImportItemInline]
    date_hierarchy = 'import_date'

@admin.register(ImportItem)
class ImportItemAdmin(admin.ModelAdmin):
    list_display = ('import_record', 'product', 'expected_quantity', 'received_quantity')
    list_filter = ('import_record__status', 'product')
    search_fields = ('import_record__reference_number', 'product__name')
    inlines = [ProductUnitInline]

@admin.register(ProductUnit)
class ProductUnitAdmin(admin.ModelAdmin):
    list_display = ('serial_number', 'product', 'status', 'created_at')
    list_filter = ('status', 'product', 'created_at')
    search_fields = ('serial_number', 'notes', 'product__name')
