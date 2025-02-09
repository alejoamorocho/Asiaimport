from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from ..domain.models.product import Product
from ..domain.models.imports import Import, ImportItem
from ..application.services.product_service import ProductService
from ..application.services.import_service import ImportService
from ..infrastructure.services.cache_service import CacheService
from ..infrastructure.repositories.product_repository import ProductRepository
from ..infrastructure.repositories.import_repository import ImportRepository
from ..application.dto.product_dto import ProductDTO
from ..application.dto.import_dto import ImportDTO, ImportItemDTO

User = get_user_model()

class ProductServiceTest(TestCase):
    """Test cases for ProductService."""
    
    def setUp(self):
        self.cache_service = CacheService()
        self.repository = ProductRepository(self.cache_service)
        self.service = ProductService(self.repository, self.cache_service)
        
        # Create test product
        self.product = Product.objects.create(
            name="Test Product",
            description="Test Description",
            sku="TEST001",
            price=Decimal("99.99"),
            stock=10
        )
    
    def test_get_product(self):
        """Test retrieving a product."""
        product_dto = self.service.get_product(self.product.id)
        self.assertIsNotNone(product_dto)
        self.assertEqual(product_dto.name, "Test Product")
        self.assertEqual(product_dto.sku, "TEST001")
    
    def test_create_product(self):
        """Test creating a new product."""
        product_dto = ProductDTO(
            id=None,
            name="New Product",
            description="New Description",
            sku="NEW001",
            barcode="123456789",
            price=Decimal("149.99"),
            stock=20,
            category_id=None
        )
        
        created_dto = self.service.create_product(product_dto)
        self.assertIsNotNone(created_dto.id)
        self.assertEqual(created_dto.name, "New Product")
        self.assertEqual(created_dto.sku, "NEW001")
    
    def test_update_product(self):
        """Test updating a product."""
        product_dto = self.service.get_product(self.product.id)
        product_dto.name = "Updated Product"
        product_dto.price = Decimal("199.99")
        
        updated_dto = self.service.update_product(product_dto)
        self.assertEqual(updated_dto.name, "Updated Product")
        self.assertEqual(updated_dto.price, Decimal("199.99"))
    
    def test_delete_product(self):
        """Test deleting a product."""
        result = self.service.delete_product(self.product.id)
        self.assertTrue(result)
        self.assertIsNone(self.service.get_product(self.product.id))

class ImportServiceTest(TestCase):
    """Test cases for ImportService."""
    
    def setUp(self):
        self.cache_service = CacheService()
        self.repository = ImportRepository(self.cache_service)
        self.service = ImportService(self.repository, self.cache_service)
        
        # Create test user
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass"
        )
        
        # Create test product
        self.product = Product.objects.create(
            name="Test Product",
            sku="TEST001",
            price=Decimal("99.99"),
            stock=10
        )
        
        # Create test import
        self.import_obj = Import.objects.create(
            status="pending",
            notes="Test Import",
            created_by=self.user
        )
        
        # Create test import item
        self.import_item = ImportItem.objects.create(
            import_file=self.import_obj,
            product=self.product,
            quantity=5,
            cost=Decimal("80.00")
        )
    
    def test_get_import(self):
        """Test retrieving an import."""
        import_dto = self.service.get_import(self.import_obj.id)
        self.assertIsNotNone(import_dto)
        self.assertEqual(import_dto.status, "pending")
        self.assertEqual(len(import_dto.items), 1)
    
    def test_create_import(self):
        """Test creating a new import."""
        import_dto = ImportDTO(
            id=None,
            status="pending",
            notes="New Import",
            created_by_id=self.user.id,
            created_at=None,
            items=[
                ImportItemDTO(
                    id=None,
                    import_id=None,
                    product_id=self.product.id,
                    quantity=3,
                    cost=Decimal("75.00")
                )
            ]
        )
        
        created_dto = self.service.create_import(import_dto)
        self.assertIsNotNone(created_dto.id)
        self.assertEqual(created_dto.status, "pending")
        self.assertEqual(len(created_dto.items), 1)
    
    def test_update_import_status(self):
        """Test updating import status."""
        updated_dto = self.service.update_import_status(
            self.import_obj.id,
            "processing"
        )
        self.assertEqual(updated_dto.status, "processing")
    
    def test_delete_import(self):
        """Test deleting an import."""
        result = self.service.delete_import(self.import_obj.id)
        self.assertTrue(result)
        self.assertIsNone(self.service.get_import(self.import_obj.id))
