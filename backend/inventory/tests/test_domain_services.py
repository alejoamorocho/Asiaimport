from django.test import TestCase
from decimal import Decimal
from ..domain.services.validation_service import ValidationService
from ..infrastructure.services.event_service import EventService
from ..domain.models.product import Product
from ..domain.models.imports import Import
from django.contrib.auth import get_user_model

User = get_user_model()

class ValidationServiceTest(TestCase):
    """Test cases for ValidationService."""
    
    def setUp(self):
        self.validation_service = ValidationService()
    
    def test_validate_product_valid_data(self):
        """Test product validation with valid data."""
        data = {
            'name': 'Test Product',
            'sku': 'TEST001',
            'price': '99.99',
            'stock': 10
        }
        errors = self.validation_service.validate_product(data)
        self.assertEqual(len(errors), 0)
    
    def test_validate_product_invalid_data(self):
        """Test product validation with invalid data."""
        data = {
            'name': '',  # Empty name
            'sku': 'TEST@001',  # Invalid SKU
            'price': '-10.00',  # Negative price
            'stock': -5  # Negative stock
        }
        errors = self.validation_service.validate_product(data)
        self.assertTrue(len(errors) > 0)
        self.assertTrue(any('name is required' in error for error in errors))
        self.assertTrue(any('SKU must be alphanumeric' in error for error in errors))
        self.assertTrue(any('Price must be greater than 0' in error for error in errors))
        self.assertTrue(any('Stock cannot be negative' in error for error in errors))
    
    def test_validate_import_valid_data(self):
        """Test import validation with valid data."""
        data = {
            'status': 'pending',
            'items': [
                {
                    'product_id': 1,
                    'quantity': 5,
                    'cost': '80.00'
                }
            ]
        }
        errors = self.validation_service.validate_import(data)
        self.assertEqual(len(errors), 0)
    
    def test_validate_import_invalid_data(self):
        """Test import validation with invalid data."""
        data = {
            'status': 'invalid_status',
            'items': [
                {
                    'product_id': None,
                    'quantity': 0,
                    'cost': '-10.00'
                }
            ]
        }
        errors = self.validation_service.validate_import(data)
        self.assertTrue(len(errors) > 0)
        self.assertTrue(any('Status must be one of:' in error for error in errors))
        self.assertTrue(any('must have a product_id' in error for error in errors))
        self.assertTrue(any('must have a positive quantity' in error for error in errors))
        self.assertTrue(any('must have a positive cost' in error for error in errors))
    
    def test_validate_import_status_transition(self):
        """Test import status transition validation."""
        # Valid transition
        errors = self.validation_service.validate_import_status_transition(
            'pending', 'processing'
        )
        self.assertEqual(len(errors), 0)
        
        # Invalid transition
        errors = self.validation_service.validate_import_status_transition(
            'completed', 'processing'
        )
        self.assertTrue(len(errors) > 0)

class EventServiceTest(TestCase):
    """Test cases for EventService."""
    
    def setUp(self):
        self.event_service = EventService()
        self.events_received = []
        
        # Create test user
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass"
        )
    
    def test_event_subscription(self):
        """Test subscribing to events."""
        def handler(data):
            self.events_received.append(data)
        
        self.event_service.subscribe('product_created', handler)
        
        # Create a product to trigger the event
        product = Product.objects.create(
            name="Test Product",
            sku="TEST001",
            price=Decimal("99.99"),
            stock=5
        )
        
        self.assertEqual(len(self.events_received), 1)
        self.assertEqual(self.events_received[0].name, "Test Product")
    
    def test_low_stock_notification(self):
        """Test low stock event handling."""
        low_stock_events = []
        
        def handler(data):
            low_stock_events.append(data)
        
        self.event_service.subscribe('product_stock_low', handler)
        
        # Create a product with low stock
        product = Product.objects.create(
            name="Low Stock Product",
            sku="LOW001",
            price=Decimal("99.99"),
            stock=2,
            stock_threshold=5
        )
        
        self.assertEqual(len(low_stock_events), 1)
        self.assertEqual(low_stock_events[0].name, "Low Stock Product")
    
    def test_import_status_change_notification(self):
        """Test import status change event handling."""
        status_change_events = []
        
        def handler(data):
            status_change_events.append(data)
        
        self.event_service.subscribe('import_status_changed', handler)
        
        # Create an import
        import_obj = Import.objects.create(
            status="pending",
            created_by=self.user
        )
        
        # Update status
        import_obj.status = "processing"
        import_obj.save()
        
        self.assertEqual(len(status_change_events), 1)
        self.assertEqual(status_change_events[0].status, "processing")
