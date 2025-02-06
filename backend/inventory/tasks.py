from celery import shared_task
from .pdf_generator import PDFGenerator
from django.core.mail import EmailMessage
from django.conf import settings
import os
from .services.import_processor import ImportProcessor

@shared_task
def generate_verification_pdf(import_id):
    """Generate verification PDF asynchronously"""
    from .models import Import  # Import here to avoid circular imports
    
    try:
        import_record = Import.objects.get(id=import_id)
        generator = PDFGenerator()
        pdf_path = generator.generate_verification_pdf(import_record)
        
        # Update import record with PDF path
        import_record.verification_pdf = pdf_path
        import_record.save()
        
        # Notify relevant users
        if settings.SEND_PDF_NOTIFICATIONS:
            subject = f'Verificación de Importación - {import_record.reference_number}'
            message = 'Se ha generado el PDF de verificación para la importación.'
            email = EmailMessage(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [import_record.created_by.email],
            )
            email.attach_file(os.path.join(settings.MEDIA_ROOT, pdf_path))
            email.send()
            
        return pdf_path
        
    except Import.DoesNotExist:
        return None
    except Exception as e:
        # Log the error
        print(f"Error generating verification PDF: {str(e)}")
        raise

@shared_task
def generate_technical_sheet_pdf(unit_id):
    """Generate technical sheet PDF asynchronously"""
    from .models import ProductUnit  # Import here to avoid circular imports
    
    try:
        unit = ProductUnit.objects.get(id=unit_id)
        generator = PDFGenerator()
        pdf_path = generator.generate_technical_sheet_pdf(unit)
        
        # Update product unit with PDF path
        unit.technical_sheet_pdf = pdf_path
        unit.save()
        
        return pdf_path
        
    except ProductUnit.DoesNotExist:
        return None
    except Exception as e:
        # Log the error
        print(f"Error generating technical sheet PDF: {str(e)}")
        raise

@shared_task
def bulk_generate_technical_sheets(unit_ids):
    """Generate technical sheets for multiple units"""
    results = []
    for unit_id in unit_ids:
        try:
            pdf_path = generate_technical_sheet_pdf(unit_id)
            results.append({'unit_id': unit_id, 'status': 'success', 'pdf_path': pdf_path})
        except Exception as e:
            results.append({'unit_id': unit_id, 'status': 'error', 'error': str(e)})
    return results

@shared_task
def process_import_file(import_id):
    """Procesa un archivo de importación de manera asíncrona."""
    from .models.import import Import  # Import here to avoid circular imports
    
    try:
        import_record = Import.objects.get(id=import_id)
        processor = ImportProcessor(import_record)
        success = processor.process()
        
        # Enviar notificación por correo
        if settings.SEND_IMPORT_NOTIFICATIONS:
            subject = f'Resultado de Importación - {import_record.id}'
            status = 'exitosa' if success else 'fallida'
            message = f'La importación ha sido {status}.'
            if not success:
                message += f'\n\nErrores encontrados:\n{import_record.error_log}'
            
            email = EmailMessage(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [import_record.created_by.email],
            )
            email.send()
        
        return {
            'success': success,
            'import_id': import_id,
            'processed_rows': import_record.processed_rows,
            'total_rows': import_record.total_rows,
            'status': import_record.status
        }
        
    except Import.DoesNotExist:
        return {'success': False, 'error': 'Importación no encontrada'}
    except Exception as e:
        return {'success': False, 'error': str(e)}
