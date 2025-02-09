# Generated by Django 4.2.19 on 2025-02-09 19:02

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Categoría', 'verbose_name_plural': 'Categorías'},
        ),
        migrations.AlterModelOptions(
            name='import',
            options={'ordering': ['-created_at'], 'verbose_name': 'Importación', 'verbose_name_plural': 'Importaciones'},
        ),
        migrations.AlterModelOptions(
            name='importitem',
            options={'ordering': ['import_file', 'row_number'], 'verbose_name': 'Item de Importación', 'verbose_name_plural': 'Items de Importación'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['name'], 'verbose_name': 'Producto', 'verbose_name_plural': 'Productos'},
        ),
        migrations.AlterModelOptions(
            name='productunit',
            options={'ordering': ['-created_at'], 'verbose_name': 'Unidad de Producto', 'verbose_name_plural': 'Unidades de Producto'},
        ),
        migrations.RemoveField(
            model_name='import',
            name='documents',
        ),
        migrations.RemoveField(
            model_name='import',
            name='import_date',
        ),
        migrations.RemoveField(
            model_name='import',
            name='notes',
        ),
        migrations.RemoveField(
            model_name='product',
            name='specifications',
        ),
        migrations.RemoveField(
            model_name='productunit',
            name='import_item',
        ),
        migrations.RemoveField(
            model_name='productunit',
            name='notes',
        ),
        migrations.AddField(
            model_name='import',
            name='error_log',
            field=models.TextField(blank=True, verbose_name='Log de Errores'),
        ),
        migrations.AddField(
            model_name='import',
            name='file',
            field=models.FileField(blank=True, default=None, null=True, upload_to='imports/%Y/%m/', verbose_name='Archivo'),
        ),
        migrations.AddField(
            model_name='import',
            name='processed_rows',
            field=models.IntegerField(default=0, verbose_name='Filas Procesadas'),
        ),
        migrations.AddField(
            model_name='import',
            name='total_rows',
            field=models.IntegerField(default=0, verbose_name='Total de Filas'),
        ),
        migrations.AddField(
            model_name='importitem',
            name='error_message',
            field=models.TextField(blank=True, verbose_name='Mensaje de Error'),
        ),
        migrations.AddField(
            model_name='importitem',
            name='import_file',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='inventory.import', verbose_name='Importación'),
        ),
        migrations.AddField(
            model_name='importitem',
            name='raw_data',
            field=models.JSONField(blank=True, default=dict, null=True, verbose_name='Datos Originales'),
        ),
        migrations.AddField(
            model_name='importitem',
            name='row_number',
            field=models.IntegerField(default=0, verbose_name='Número de Fila'),
        ),
        migrations.AddField(
            model_name='importitem',
            name='status',
            field=models.CharField(choices=[('pending', 'Pendiente'), ('success', 'Éxito'), ('error', 'Error')], default='pending', max_length=20, verbose_name='Estado'),
        ),
        migrations.AddField(
            model_name='product',
            name='barcode',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True, verbose_name='Código de Barras'),
        ),
        migrations.AddField(
            model_name='product',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Activo'),
        ),
        migrations.AddField(
            model_name='product',
            name='last_purchase_date',
            field=models.DateField(blank=True, null=True, verbose_name='Última Fecha de Compra'),
        ),
        migrations.AddField(
            model_name='product',
            name='last_purchase_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Último Precio de Compra'),
        ),
        migrations.AddField(
            model_name='product',
            name='min_stock',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Stock Mínimo'),
        ),
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1000000)], verbose_name='Precio'),
        ),
        migrations.AddField(
            model_name='product',
            name='sku',
            field=models.CharField(blank=True, default=None, max_length=50, null=True, unique=True, verbose_name='SKU'),
        ),
        migrations.AddField(
            model_name='product',
            name='stock',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100000)], verbose_name='Stock'),
        ),
        migrations.AddField(
            model_name='productunit',
            name='technical_sheet',
            field=models.FileField(blank=True, null=True, upload_to='technical_sheets/', verbose_name='Ficha Técnica'),
        ),
        migrations.AlterField(
            model_name='category',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación'),
        ),
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.TextField(blank=True, verbose_name='Descripción'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=50, unique=True, verbose_name='Nombre'),
        ),
        migrations.AlterField(
            model_name='category',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización'),
        ),
        migrations.AlterField(
            model_name='import',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación'),
        ),
        migrations.AlterField(
            model_name='import',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='imports', to=settings.AUTH_USER_MODEL, verbose_name='Creado por'),
        ),
        migrations.AlterField(
            model_name='import',
            name='reference_number',
            field=models.CharField(max_length=50, unique=True, verbose_name='Número de Referencia'),
        ),
        migrations.AlterField(
            model_name='import',
            name='status',
            field=models.CharField(choices=[('pending', 'Pendiente'), ('processing', 'Procesando'), ('completed', 'Completado'), ('failed', 'Fallido')], default='pending', max_length=20, verbose_name='Estado'),
        ),
        migrations.AlterField(
            model_name='import',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización'),
        ),
        migrations.AlterField(
            model_name='importitem',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación'),
        ),
        migrations.AlterField(
            model_name='importitem',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='import_items', to='inventory.product', verbose_name='Producto'),
        ),
        migrations.AlterField(
            model_name='importitem',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización'),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products', to='inventory.category', verbose_name='Categoría'),
        ),
        migrations.AlterField(
            model_name='product',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(verbose_name='Descripción'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Nombre'),
        ),
        migrations.AlterField(
            model_name='product',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización'),
        ),
        migrations.AlterField(
            model_name='productunit',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación'),
        ),
        migrations.AlterField(
            model_name='productunit',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='units', to='inventory.product', verbose_name='Producto'),
        ),
        migrations.AlterField(
            model_name='productunit',
            name='serial_number',
            field=models.CharField(max_length=100, unique=True, verbose_name='Número de Serie'),
        ),
        migrations.AlterField(
            model_name='productunit',
            name='status',
            field=models.CharField(choices=[('available', 'Disponible'), ('sold', 'Vendido'), ('reserved', 'Reservado'), ('damaged', 'Dañado')], default='available', max_length=20, verbose_name='Estado'),
        ),
        migrations.AlterField(
            model_name='productunit',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización'),
        ),
        migrations.AlterUniqueTogether(
            name='importitem',
            unique_together={('import_file', 'row_number')},
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['name'], name='inventory_p_name_f6a6a1_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['sku'], name='inventory_p_sku_f85905_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['barcode'], name='inventory_p_barcode_3a77e5_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['category'], name='inventory_p_categor_607069_idx'),
        ),
        migrations.RemoveField(
            model_name='importitem',
            name='expected_quantity',
        ),
        migrations.RemoveField(
            model_name='importitem',
            name='import_record',
        ),
        migrations.RemoveField(
            model_name='importitem',
            name='notes',
        ),
        migrations.RemoveField(
            model_name='importitem',
            name='received_quantity',
        ),
    ]
