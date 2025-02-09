from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from .base import BaseModel


class Category(BaseModel):
    name = models.CharField(max_length=50, unique=True, verbose_name="Nombre")
    description = models.TextField(blank=True, verbose_name="Descripción")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"


class Product(BaseModel):
    name = models.CharField(max_length=100, verbose_name="Nombre")
    description = models.TextField(verbose_name="Descripción")
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(1000000)],
        verbose_name="Precio",
        default=0
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
        verbose_name="Categoría"
    )
    stock = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100000)],
        verbose_name="Stock"
    )
    sku = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="SKU",
        null=True,
        blank=True,
        default=None
    )
    barcode = models.CharField(
        max_length=100,
        unique=True,
        null=True,
        blank=True,
        verbose_name="Código de Barras"
    )
    min_stock = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Stock Mínimo"
    )
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    last_purchase_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name="Último Precio de Compra"
    )
    last_purchase_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Última Fecha de Compra"
    )

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["sku"]),
            models.Index(fields=["barcode"]),
            models.Index(fields=["category"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.sku})"

    def save(self, *args, **kwargs):
        if not self.sku:
            # Generar SKU automáticamente si no se proporciona
            last_product = Product.objects.order_by("-id").first()
            last_id = last_product.id if last_product else 0
            self.sku = f"PRD{str(last_id + 1).zfill(6)}"
        super().save(*args, **kwargs)

    @property
    def needs_restock(self):
        """Indica si el producto necesita reabastecimiento."""
        return self.stock <= self.min_stock

    @property
    def stock_status(self):
        """Devuelve el estado del stock."""
        if self.stock <= self.min_stock:
            return "low"
        elif self.stock <= self.min_stock * 2:
            return "medium"
        return "good"

    @property
    def category_name(self):
        return self.category.name if self.category else None

    @property
    def unit_symbol(self):
        return None
