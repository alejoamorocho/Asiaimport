from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .validators import (
    validate_reference_number,
    validate_serial_number,
    validate_specifications,
    validate_import_date,
    validate_received_quantity,
    validate_status_transition
)

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

class Product(models.Model):
    name = models.CharField(max_length=200, unique=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    description = models.TextField()
    specifications = models.JSONField(default=dict, validators=[validate_specifications])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Import(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    reference_number = models.CharField(
        max_length=100,
        unique=True,
        validators=[validate_reference_number]
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    import_date = models.DateField(validators=[validate_import_date])
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    documents = models.FileField(upload_to='imports/documents/', blank=True, null=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Import {self.reference_number}"

    class Meta:
        ordering = ['-import_date', '-created_at']

class ImportItem(models.Model):
    import_record = models.ForeignKey(Import, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    expected_quantity = models.PositiveIntegerField()
    received_quantity = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.received_quantity:
            validate_received_quantity(self.received_quantity, self.expected_quantity)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - {self.import_record.reference_number}"

    class Meta:
        ordering = ['-created_at']

class ProductUnit(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('in_use', 'In Use'),
        ('maintenance', 'Under Maintenance'),
        ('defective', 'Defective'),
        ('disposed', 'Disposed'),
    ]

    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='units')
    import_item = models.ForeignKey(ImportItem, on_delete=models.PROTECT, related_name='units')
    serial_number = models.CharField(
        max_length=100,
        unique=True,
        validators=[validate_serial_number]
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.import_item.received_quantity >= self.import_item.expected_quantity:
            raise ValidationError(
                'No se pueden agregar más unidades. La cantidad recibida ya alcanzó la cantidad esperada.'
            )
        
        if self.pk:  # Si la unidad ya existe, validar la transición de estado
            original = ProductUnit.objects.get(pk=self.pk)
            if original.status != self.status:
                validate_status_transition(original.status, self.status)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
        # Actualizar la cantidad recibida del ImportItem
        self.import_item.received_quantity = self.import_item.units.count()
        self.import_item.save()

    def __str__(self):
        return f"{self.product.name} - {self.serial_number}"

    class Meta:
        ordering = ['-created_at']
