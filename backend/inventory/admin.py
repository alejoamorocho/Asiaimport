from django.contrib import admin
from .models import Category, Product, Import, ImportItem, ProductUnit

class ProductUnitInline(admin.TabularInline):
    model = ProductUnit
    extra = 0
    fields = ('serial_number', 'status', 'technical_sheet')

class ImportItemInline(admin.TabularInline):
    model = ImportItem
    extra = 1

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
    inlines = [ProductUnitInline]

@admin.register(Import)
class ImportAdmin(admin.ModelAdmin):
    list_display = ('reference_number', 'status', 'created_at', 'created_by')
    list_filter = ('status', 'created_at')
    search_fields = ('reference_number',)
    inlines = [ImportItemInline]
    date_hierarchy = 'created_at'

@admin.register(ImportItem)
class ImportItemAdmin(admin.ModelAdmin):
    list_display = ('import_file', 'product', 'row_number', 'status')
    list_filter = ('import_file__status', 'status', 'product')
    search_fields = ('import_file__id', 'product__name')

@admin.register(ProductUnit)
class ProductUnitAdmin(admin.ModelAdmin):
    list_display = ('serial_number', 'product', 'status', 'created_at')
    list_filter = ('status', 'product', 'created_at')
    search_fields = ('serial_number', 'notes', 'product__name')
