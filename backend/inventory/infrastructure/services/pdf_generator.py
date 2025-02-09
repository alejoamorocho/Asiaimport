"""
PDF Generator service for generating various PDF documents.
"""

import os
from django.conf import settings
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch


class PDFGenerator:
    """Generates PDF documents for various purposes."""

    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.custom_style = ParagraphStyle(
            'CustomStyle',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=20
        )

    def generate_verification_pdf(self, import_record):
        """Generate a verification PDF for an import record."""
        filename = f'verification_{import_record.reference_number}.pdf'
        filepath = os.path.join(settings.MEDIA_ROOT, 'pdfs', filename)
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Create PDF
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        elements = []
        
        # Title
        title = Paragraph(f'Verificación de Importación - {import_record.reference_number}', self.styles['Title'])
        elements.append(title)
        
        # Import details
        elements.append(Paragraph(f'Fecha: {import_record.import_date}', self.custom_style))
        elements.append(Paragraph(f'Estado: {import_record.status}', self.custom_style))
        elements.append(Paragraph(f'Creado por: {import_record.created_by}', self.custom_style))
        
        # Items table
        items_data = [['Producto', 'Cantidad Esperada', 'Cantidad Recibida', 'Estado']]
        for item in import_record.items.all():
            items_data.append([
                item.product.name,
                str(item.expected_quantity),
                str(item.received_quantity),
                item.status
            ])
        
        table = Table(items_data, colWidths=[3*inch, 1.5*inch, 1.5*inch, 1.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 12),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(table)
        
        # Build PDF
        doc.build(elements)
        return filepath

    def generate_technical_sheet_pdf(self, unit):
        """Generate a technical sheet PDF for a product unit."""
        filename = f'technical_sheet_{unit.serial_number}.pdf'
        filepath = os.path.join(settings.MEDIA_ROOT, 'pdfs', filename)
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Create PDF
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        elements = []
        
        # Title
        title = Paragraph(f'Ficha Técnica - {unit.product.name}', self.styles['Title'])
        elements.append(title)
        
        # Product details
        elements.append(Paragraph(f'Número de Serie: {unit.serial_number}', self.custom_style))
        elements.append(Paragraph(f'Estado: {unit.status}', self.custom_style))
        elements.append(Paragraph(f'Categoría: {unit.product.category.name}', self.custom_style))
        
        # Specifications table
        if unit.product.specifications:
            elements.append(Paragraph('Especificaciones:', self.styles['Heading2']))
            specs_data = [['Característica', 'Valor']]
            for key, value in unit.product.specifications.items():
                specs_data.append([key, str(value)])
            
            table = Table(specs_data, colWidths=[3*inch, 4*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 14),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 12),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elements.append(table)
        
        # Build PDF
        doc.build(elements)
        return filepath
