"""
ProductUnit model definition.
"""
from django.db import models
from .base import BaseModel
from .product import Product


class ProductUnit(BaseModel):
    """
    Model representing a specific unit of a product.
    """
    STATUS_CHOICES = [
        ('available', 'Disponible'),
        ('sold', 'Vendido'),
        ('reserved', 'Reservado'),
        ('damaged', 'Dañado'),
    ]

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='units',
        verbose_name='Producto'
    )
    serial_number = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Número de Serie'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='available',
        verbose_name='Estado'
    )
    technical_sheet = models.FileField(
        upload_to='technical_sheets/',
        null=True,
        blank=True,
        verbose_name='Ficha Técnica'
    )

    class Meta:
        verbose_name = 'Unidad de Producto'
        verbose_name_plural = 'Unidades de Producto'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.product.name} - {self.serial_number}"
