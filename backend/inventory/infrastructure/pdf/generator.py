from django.template.loader import render_to_string
from django.conf import settings
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
import os
from datetime import datetime

class PDFGenerator:
    def __init__(self):
        self.font_config = FontConfiguration()
        self.css_path = os.path.join(settings.STATIC_ROOT, 'css', 'pdf.css')
        
    def _get_pdf_filename(self, prefix):
        """Generate a unique filename for the PDF"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return f"{prefix}_{timestamp}.pdf"
        
    def generate_verification_pdf(self, import_record):
        """Generate verification PDF for an import record"""
        context = {
            'import': import_record,
            'items': import_record.items.all(),
            'company_name': settings.COMPANY_NAME,
            'company_logo': settings.COMPANY_LOGO,
            'generated_at': datetime.now(),
        }
        
        html_string = render_to_string('inventory/pdf/verification.html', context)
        html = HTML(string=html_string, base_url=settings.STATIC_URL)
        
        # Apply custom CSS
        css = []
        if os.path.exists(self.css_path):
            css.append(CSS(filename=self.css_path, font_config=self.font_config))
            
        # Generate PDF
        filename = self._get_pdf_filename(f'verification_{import_record.reference_number}')
        output_path = os.path.join(settings.MEDIA_ROOT, 'pdfs', filename)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        html.write_pdf(
            output_path,
            stylesheets=css,
            font_config=self.font_config,
            presentational_hints=True
        )
        
        return os.path.join('pdfs', filename)
        
    def generate_technical_sheet_pdf(self, product_unit):
        """Generate technical sheet PDF for a product unit"""
        context = {
            'unit': product_unit,
            'product': product_unit.product,
            'import': product_unit.import_item.import_record,
            'company_name': settings.COMPANY_NAME,
            'company_logo': settings.COMPANY_LOGO,
            'generated_at': datetime.now(),
        }
        
        html_string = render_to_string('inventory/pdf/technical_sheet.html', context)
        html = HTML(string=html_string, base_url=settings.STATIC_URL)
        
        # Apply custom CSS
        css = []
        if os.path.exists(self.css_path):
            css.append(CSS(filename=self.css_path, font_config=self.font_config))
            
        # Generate PDF
        filename = self._get_pdf_filename(f'technical_sheet_{product_unit.serial_number}')
        output_path = os.path.join(settings.MEDIA_ROOT, 'pdfs', filename)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        html.write_pdf(
            output_path,
            stylesheets=css,
            font_config=self.font_config,
            presentational_hints=True
        )
        
        return os.path.join('pdfs', filename)
