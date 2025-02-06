from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from inventory.models import Category, Product, Import, ImportItem, ProductUnit
from datetime import date

class CategoryAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass'
        )
        self.client.force_authenticate(user=self.user)
        self.category_data = {
            'name': 'Test Category',
            'description': 'Test Description'
        }

    def test_create_category(self):
        response = self.client.post(
            reverse('category-list'),
            self.category_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(Category.objects.get().name, 'Test Category')

    def test_get_categories(self):
        Category.objects.create(**self.category_data)
        response = self.client.get(reverse('category-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

class ProductAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass'
        )
        self.client.force_authenticate(user=self.user)
        self.category = Category.objects.create(name='Test Category')
        self.product_data = {
            'name': 'Test Product',
            'category': self.category.id,
            'description': 'Test Description',
            'specifications': {
                'potencia': 100,
                'peso': 5.5,
                'dimensiones': '30x20x10',
                'voltaje': 220,
                'frecuencia': 50
            }
        }

    def test_create_product(self):
        response = self.client.post(
            reverse('product-list'),
            self.product_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.get().name, 'Test Product')

    def test_invalid_product_creation(self):
        invalid_data = self.product_data.copy()
        invalid_data['specifications'] = {'invalid': 'spec'}
        response = self.client.post(
            reverse('product-list'),
            invalid_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class ImportAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass'
        )
        self.client.force_authenticate(user=self.user)
        self.import_data = {
            'reference_number': f'IMP-{date.today().year}-001',
            'status': 'pending',
            'import_date': date.today().isoformat(),
            'notes': 'Test Import'
        }

    def test_create_import(self):
        response = self.client.post(
            reverse('import-list'),
            self.import_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Import.objects.count(), 1)
        import_obj = Import.objects.get()
        self.assertEqual(import_obj.created_by, self.user)

    def test_invalid_import_creation(self):
        invalid_data = self.import_data.copy()
        invalid_data['reference_number'] = 'INVALID'
        response = self.client.post(
            reverse('import-list'),
            invalid_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class PDFGenerationAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass'
        )
        self.client.force_authenticate(user=self.user)
        
        # Create necessary objects
        self.category = Category.objects.create(name='Test Category')
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

    def test_generate_verification_pdf(self):
        response = self.client.post(
            reverse('generate-verification-pdf', kwargs={'pk': self.import_obj.pk}),
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertIn('task_id', response.data)

    def test_generate_technical_sheet_pdf(self):
        import_item = ImportItem.objects.create(
            import_record=self.import_obj,
            product=self.product,
            expected_quantity=1
        )
        unit = ProductUnit.objects.create(
            product=self.product,
            import_item=import_item,
            serial_number='LPX1-2024-001',
            status='available'
        )
        
        response = self.client.post(
            reverse('generate-technical-sheet-pdf', kwargs={'pk': unit.pk}),
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertIn('task_id', response.data)
