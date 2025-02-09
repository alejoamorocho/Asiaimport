"""
Tasks module for background processing.
This module contains all the Celery tasks for background processing.
"""

from celery import shared_task
from ...infrastructure.services.pdf_generator import PDFGenerator
from django.core.mail import EmailMessage
from django.conf import settings
import os
from ..services.import_processor import ImportProcessor

@shared_task
def generate_verification_pdf(import_id):
    """Generate verification PDF asynchronously"""
    from ...domain.models import Import  # Import here to avoid circular imports
    
    try:
        import_record = Import.objects.get(id=import_id)
        generator = PDFGenerator()
        pdf_path = generator.generate_verification_pdf(import_record)
        
        # Update import record with PDF path
        import_record.verification_pdf = pdf_path
        import_record.save()
        
        return {
            'status': 'success',
            'message': 'PDF generado correctamente',
            'path': pdf_path
        }
    except Import.DoesNotExist:
        return {
            'status': 'error',
            'message': 'Importación no encontrada'
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e)
        }

@shared_task
def generate_technical_sheet_pdf(unit_id):
    """Generate technical sheet PDF asynchronously"""
    from ...domain.models import ProductUnit  # Import here to avoid circular imports
    
    try:
        unit = ProductUnit.objects.get(id=unit_id)
        generator = PDFGenerator()
        pdf_path = generator.generate_technical_sheet_pdf(unit)
        
        # Update unit with PDF path
        unit.technical_sheet = pdf_path
        unit.save()
        
        return {
            'status': 'success',
            'message': 'Ficha técnica generada correctamente',
            'path': pdf_path
        }
    except ProductUnit.DoesNotExist:
        return {
            'status': 'error',
            'message': 'Unidad no encontrada'
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e)
        }

@shared_task
def bulk_generate_technical_sheets(unit_ids):
    """Generate technical sheets for multiple units"""
    results = []
    for unit_id in unit_ids:
        result = generate_technical_sheet_pdf.delay(unit_id)
        results.append(result.id)
    return results

@shared_task
def process_import_file(import_id):
    """Procesa un archivo de importación de manera asíncrona."""
    from ...domain.models import Import  # Import here to avoid circular imports
    
    try:
        import_record = Import.objects.get(id=import_id)
        processor = ImportProcessor()
        result = processor.process_file(import_record)
        
        # Send email notification
        if result['status'] == 'success':
            subject = 'Importación procesada correctamente'
            message = f'La importación {import_record.reference_number} ha sido procesada correctamente.'
        else:
            subject = 'Error en el procesamiento de la importación'
            message = f'Ha ocurrido un error al procesar la importación {import_record.reference_number}:\n{result["message"]}'
        
        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[import_record.created_by.email],
        )
        email.send()
        
        return result
    except Import.DoesNotExist:
        return {
            'status': 'error',
            'message': 'Importación no encontrada'
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e)
        }
