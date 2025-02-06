import pandas as pd
from typing import Dict, List, Tuple
from django.db import transaction
from ..models.import import Import, ImportItem
from ..models.product import Product
from ..models.category import Category


class ImportProcessor:
    """Procesa archivos de importación de productos."""

    REQUIRED_COLUMNS = {
        'nombre': 'name',
        'descripcion': 'description',
        'precio': 'price',
        'categoria': 'category',
        'stock': 'stock',
        'codigo_barras': 'barcode',
        'stock_minimo': 'min_stock'
    }

    def __init__(self, import_obj: Import):
        self.import_obj = import_obj
        self.errors = []
        self.processed_items = []

    def process(self) -> bool:
        """Procesa el archivo de importación."""
        try:
            # Actualizar estado
            self.import_obj.status = 'processing'
            self.import_obj.save()

            # Leer archivo
            df = self._read_file()
            if df is None:
                return False

            # Validar columnas
            if not self._validate_columns(df.columns):
                return False

            # Procesar filas
            self.import_obj.total_rows = len(df)
            self.import_obj.save()

            # Procesar cada fila
            for index, row in df.iterrows():
                self._process_row(index + 2, row)  # +2 porque Excel empieza en 1 y tiene encabezados
                self.import_obj.processed_rows += 1
                self.import_obj.save()

            # Actualizar estado final
            success = len(self.errors) == 0
            self.import_obj.status = 'completed' if success else 'failed'
            self.import_obj.error_log = '\n'.join(self.errors)
            self.import_obj.save()

            return success

        except Exception as e:
            self.import_obj.status = 'failed'
            self.import_obj.error_log = f"Error general: {str(e)}"
            self.import_obj.save()
            return False

    def _read_file(self) -> pd.DataFrame:
        """Lee el archivo de importación."""
        try:
            file_path = self.import_obj.file.path
            if file_path.endswith('.csv'):
                return pd.read_csv(file_path)
            return pd.read_excel(file_path)
        except Exception as e:
            self.errors.append(f"Error al leer el archivo: {str(e)}")
            return None

    def _validate_columns(self, columns: List[str]) -> bool:
        """Valida que el archivo tenga las columnas requeridas."""
        columns = [col.lower().strip() for col in columns]
        missing_columns = [
            col for col in self.REQUIRED_COLUMNS.keys()
            if col not in columns
        ]

        if missing_columns:
            self.errors.append(
                f"Faltan las siguientes columnas requeridas: {', '.join(missing_columns)}"
            )
            return False
        return True

    def _process_row(self, row_number: int, row: pd.Series) -> None:
        """Procesa una fila del archivo."""
        try:
            # Limpiar y validar datos
            data = self._clean_row_data(row)
            if not data:
                return

            # Crear o actualizar producto
            with transaction.atomic():
                product = self._create_or_update_product(data)
                
                # Crear item de importación
                ImportItem.objects.create(
                    import_file=self.import_obj,
                    row_number=row_number,
                    status='success',
                    product=product,
                    raw_data=data
                )

        except Exception as e:
            error_msg = f"Error en la fila {row_number}: {str(e)}"
            self.errors.append(error_msg)
            ImportItem.objects.create(
                import_file=self.import_obj,
                row_number=row_number,
                status='error',
                error_message=error_msg,
                raw_data=row.to_dict()
            )

    def _clean_row_data(self, row: pd.Series) -> Dict:
        """Limpia y valida los datos de una fila."""
        try:
            data = {}
            for spanish_col, english_col in self.REQUIRED_COLUMNS.items():
                value = row[spanish_col]
                
                # Validaciones específicas por campo
                if english_col == 'price':
                    value = float(value)
                    if value < 0:
                        raise ValueError("El precio no puede ser negativo")
                
                elif english_col == 'stock':
                    value = int(value)
                    if value < 0:
                        raise ValueError("El stock no puede ser negativo")
                
                elif english_col == 'min_stock':
                    value = int(value)
                    if value < 0:
                        raise ValueError("El stock mínimo no puede ser negativo")
                
                data[english_col] = value
            
            return data
        
        except Exception as e:
            self.errors.append(f"Error al procesar fila: {str(e)}")
            return None

    def _create_or_update_product(self, data: Dict) -> Product:
        """Crea o actualiza un producto."""
        # Buscar o crear categoría
        category_name = data.pop('category')
        category, _ = Category.objects.get_or_create(
            name=category_name,
            defaults={'is_active': True}
        )

        # Buscar producto existente por código de barras
        product = None
        if data.get('barcode'):
            product = Product.objects.filter(barcode=data['barcode']).first()

        if product:
            # Actualizar producto existente
            for key, value in data.items():
                setattr(product, key, value)
            product.category = category
            product.save()
        else:
            # Crear nuevo producto
            product = Product.objects.create(
                category=category,
                **data
            )

        return product
