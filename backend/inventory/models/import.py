from django.db import models
from django.conf import settings
from .base import BaseModel
from .product import Product


class Import(BaseModel):
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('processing', 'Procesando'),
        ('completed', 'Completado'),
        ('failed', 'Fallido'),
    ]

    file = models.FileField(
        upload_to='imports/%Y/%m/',
        verbose_name="Archivo"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Estado"
    )
    processed_rows = models.IntegerField(
        default=0,
        verbose_name="Filas Procesadas"
    )
    total_rows = models.IntegerField(
        default=0,
        verbose_name="Total de Filas"
    )
    error_log = models.TextField(
        blank=True,
        verbose_name="Log de Errores"
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='imports',
        verbose_name="Creado por"
    )

    class Meta:
        verbose_name = "Importación"
        verbose_name_plural = "Importaciones"
        ordering = ['-created_at']

    def __str__(self):
        return f"Importación {self.id} - {self.get_status_display()}"


class ImportItem(BaseModel):
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('success', 'Éxito'),
        ('error', 'Error'),
    ]

    import_file = models.ForeignKey(
        Import,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="Importación"
    )
    row_number = models.IntegerField(
        verbose_name="Número de Fila"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Estado"
    )
    error_message = models.TextField(
        blank=True,
        verbose_name="Mensaje de Error"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='import_items',
        verbose_name="Producto"
    )
    raw_data = models.JSONField(
        verbose_name="Datos Originales"
    )

    class Meta:
        verbose_name = "Item de Importación"
        verbose_name_plural = "Items de Importación"
        ordering = ['import_file', 'row_number']
        unique_together = [['import_file', 'row_number']]

    def __str__(self):
        return f"Item {self.row_number} de Importación {self.import_file_id}"
