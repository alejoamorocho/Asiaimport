"""
Service for processing import files.
"""

import pandas as pd
from django.db import transaction
from ...domain.models import Product, Category


class ImportProcessor:
    """Processes import files and creates/updates records."""

    def process_file(self, import_record):
        """Process an import file and create/update records."""
        try:
            # Read the file
            df = pd.read_excel(import_record.file.path)
            
            # Update import status
            import_record.status = 'in_progress'
            import_record.save()
            
            # Process each row
            with transaction.atomic():
                for index, row in df.iterrows():
                    try:
                        # Get or create category
                        category, _ = Category.objects.get_or_create(
                            name=row['category'],
                            defaults={'description': row.get('category_description', '')}
                        )
                        
                        # Get or create product
                        product, created = Product.objects.get_or_create(
                            name=row['product_name'],
                            defaults={
                                'category': category,
                                'description': row.get('description', ''),
                                'specifications': {
                                    'brand': row.get('brand', ''),
                                    'model': row.get('model', ''),
                                    'dimensions': row.get('dimensions', ''),
                                    'weight': row.get('weight', ''),
                                    'color': row.get('color', ''),
                                }
                            }
                        )
                        
                        # Create import item
                        import_record.items.create(
                            product=product,
                            expected_quantity=row['quantity'],
                            row_number=index + 2,  # Excel starts at 1 and has header
                            status='success'
                        )
                        
                    except KeyError as e:
                        # Create error item
                        import_record.items.create(
                            row_number=index + 2,
                            status='error',
                            error_message=f'Columna requerida no encontrada: {str(e)}',
                            raw_data=row.to_dict()
                        )
                    except Exception as e:
                        # Create error item
                        import_record.items.create(
                            row_number=index + 2,
                            status='error',
                            error_message=str(e),
                            raw_data=row.to_dict()
                        )
            
            # Update import status
            success_count = import_record.items.filter(status='success').count()
            error_count = import_record.items.filter(status='error').count()
            
            if error_count == 0:
                import_record.status = 'completed'
            elif success_count == 0:
                import_record.status = 'failed'
            else:
                import_record.status = 'completed_with_errors'
            
            import_record.save()
            
            return {
                'status': 'success',
                'message': f'Procesamiento completado. {success_count} registros exitosos, {error_count} errores.',
                'success_count': success_count,
                'error_count': error_count
            }
            
        except Exception as e:
            import_record.status = 'failed'
            import_record.save()
            
            return {
                'status': 'error',
                'message': str(e)
            }
