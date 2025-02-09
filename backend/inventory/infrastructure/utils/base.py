from django.template.loader import render_to_string
from django.conf import settings
from weasyprint import HTML
import tempfile

def generate_import_report(import_obj):
    """Generate a PDF report for import verification"""
    context = {
        'import': import_obj,
        'items': import_obj.items.all().select_related('product'),
    }
    
    html_string = render_to_string('inventory/reports/import_verification.html', context)
    
    # Create a temporary file to store the PDF
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as pdf_file:
        HTML(string=html_string).write_pdf(
            pdf_file.name,
            stylesheets=[settings.STATIC_ROOT / 'css/reports.css']
        )
        return open(pdf_file.name, 'rb').read()

def generate_product_technical_sheet(product):
    """Generate a PDF technical sheet for a product"""
    context = {
        'product': product,
        'specifications': product.specifications,
    }
    
    html_string = render_to_string('inventory/reports/technical_sheet.html', context)
    
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as pdf_file:
        HTML(string=html_string).write_pdf(
            pdf_file.name,
            stylesheets=[settings.STATIC_ROOT / 'css/reports.css']
        )
        return open(pdf_file.name, 'rb').read()
