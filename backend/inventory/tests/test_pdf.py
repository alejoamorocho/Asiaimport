from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.conf import settings
from inventory.models import Category, Product, Import, ImportItem, ProductUnit
from inventory.pdf_generator import PDFGenerator
from datetime import date
import os
import shutil

class PDFGeneratorTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Crear directorio temporal para PDFs
        cls.test_media_root = os.path.join(settings.BASE_DIR, 'test_media')
        settings.MEDIA_ROOT = cls.test_media_root
        os.makedirs(os.path.join(cls.test_media_root, 'pdfs'), exist_ok=True)

    @classmethod
    def tearDownClass(cls):
        # Limpiar archivos de prueba
        shutil.rmtree(cls.test_media_root, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        self.pdf_generator = PDFGenerator()
        
        # Crear datos de prueba
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        
        self.category = Category.objects.create(
            name='Test Category',
            description='Test Description'
        )
        
        self.product = Product.objects.create(
            name='Test Product',
            category=self.category,
            description='Test Description',
            specifications={
                'potencia': 100,
                'peso': 5.5,
                'dimensiones': '30x20x10',
                'voltaje': 220,
                'frecuencia': 50
            }
        )
        
        self.import_obj = Import.objects.create(
            reference_number=f'IMP-{date.today().year}-001',
            status='pending',
            import_date=date.today(),
            created_by=self.user
        )
        
        self.import_item = ImportItem.objects.create(
            import_record=self.import_obj,
            product=self.product,
            expected_quantity=1
        )
        
        self.product_unit = ProductUnit.objects.create(
            product=self.product,
            import_item=self.import_item,
            serial_number=f'LPX1-{date.today().year}-001',
            status='available'
        )

    def test_verification_pdf_generation(self):
        """Prueba la generación del PDF de verificación"""
        pdf_path = self.pdf_generator.generate_verification_pdf(self.import_obj)
        
        # Verificar que el archivo existe
        self.assertTrue(default_storage.exists(pdf_path))
        
        # Verificar que el archivo es un PDF válido
        with default_storage.open(pdf_path, 'rb') as pdf_file:
            self.assertTrue(pdf_file.read().startswith(b'%PDF'))

    def test_technical_sheet_pdf_generation(self):
        """Prueba la generación del PDF de ficha técnica"""
        pdf_path = self.pdf_generator.generate_technical_sheet_pdf(self.product_unit)
        
        # Verificar que el archivo existe
        self.assertTrue(default_storage.exists(pdf_path))
        
        # Verificar que el archivo es un PDF válido
        with default_storage.open(pdf_path, 'rb') as pdf_file:
            self.assertTrue(pdf_file.read().startswith(b'%PDF'))

    def test_pdf_filename_format(self):
        """Prueba el formato de nombres de archivo PDF"""
        # Verificación
        verification_path = self.pdf_generator.generate_verification_pdf(self.import_obj)
        self.assertRegex(
            verification_path,
            r'pdfs/verification_IMP-\d{4}-001_\d{8}_\d{6}\.pdf'
        )
        
        # Ficha técnica
        technical_path = self.pdf_generator.generate_technical_sheet_pdf(self.product_unit)
        self.assertRegex(
            technical_path,
            r'pdfs/technical_sheet_LPX1-\d{4}-001_\d{8}_\d{6}\.pdf'
        )

    def test_pdf_content_verification(self):
        """Prueba el contenido del PDF de verificación"""
        from weasyprint import HTML
        
        # Generar PDF
        pdf_path = self.pdf_generator.generate_verification_pdf(self.import_obj)
        full_path = os.path.join(settings.MEDIA_ROOT, pdf_path)
        
        # Extraer texto del PDF
        html = HTML(filename=full_path)
        text = ' '.join([page.text for page in html.pages])
        
        # Verificar contenido esperado
        self.assertIn(self.import_obj.reference_number, text)
        self.assertIn(self.product.name, text)
        self.assertIn(str(self.import_item.expected_quantity), text)

    def test_pdf_content_technical_sheet(self):
        """Prueba el contenido del PDF de ficha técnica"""
        from weasyprint import HTML
        
        # Generar PDF
        pdf_path = self.pdf_generator.generate_technical_sheet_pdf(self.product_unit)
        full_path = os.path.join(settings.MEDIA_ROOT, pdf_path)
        
        # Extraer texto del PDF
        html = HTML(filename=full_path)
        text = ' '.join([page.text for page in html.pages])
        
        # Verificar contenido esperado
        self.assertIn(self.product.name, text)
        self.assertIn(self.product_unit.serial_number, text)
        self.assertIn(str(self.product.specifications['potencia']), text)
        self.assertIn(self.product.specifications['dimensiones'], text)
