from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils import timezone
from inventory.models import Category, Product, Import, ImportItem, ProductUnit
from datetime import date, timedelta

class CategoryTests(TestCase):
    def test_category_creation(self):
        category = Category.objects.create(
            name="Test Category",
            description="Test Description"
        )
        self.assertEqual(str(category), "Test Category")
        self.assertTrue(category.created_at)
        self.assertTrue(category.updated_at)

    def test_unique_name(self):
        Category.objects.create(name="Test Category")
        with self.assertRaises(Exception):
            Category.objects.create(name="Test Category")

class ProductTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Test Category",
            description="Test Description"
        )

    def test_product_creation(self):
        product = Product.objects.create(
            name="Test Product",
            category=self.category,
            description="Test Description",
            specifications={
                "potencia": 100,
                "peso": 5.5,
                "dimensiones": "30x20x10",
                "voltaje": 220,
                "frecuencia": 50
            }
        )
        self.assertEqual(str(product), "Test Product")
        self.assertEqual(product.category, self.category)

    def test_invalid_specifications(self):
        with self.assertRaises(ValidationError):
            Product.objects.create(
                name="Invalid Product",
                category=self.category,
                description="Test",
                specifications={"invalid": "spec"}
            )

class ImportTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass"
        )

    def test_import_creation(self):
        import_obj = Import.objects.create(
            reference_number=f"IMP-{date.today().year}-001",
            status="pending",
            import_date=date.today(),
            created_by=self.user
        )
        self.assertEqual(str(import_obj), f"Import IMP-{date.today().year}-001")
        self.assertEqual(import_obj.status, "pending")

    def test_invalid_reference_number(self):
        with self.assertRaises(ValidationError):
            Import.objects.create(
                reference_number="INVALID-REF",
                status="pending",
                import_date=date.today(),
                created_by=self.user
            )

    def test_future_import_date(self):
        with self.assertRaises(ValidationError):
            Import.objects.create(
                reference_number=f"IMP-{date.today().year}-001",
                status="pending",
                import_date=date.today() + timedelta(days=1),
                created_by=self.user
            )

class ImportItemTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Test Category")
        self.product = Product.objects.create(
            name="Test Product",
            category=self.category,
            description="Test Description",
            specifications={
                "potencia": 100,
                "peso": 5.5,
                "dimensiones": "30x20x10",
                "voltaje": 220,
                "frecuencia": 50
            }
        )
        self.user = User.objects.create_user(username="testuser")
        self.import_obj = Import.objects.create(
            reference_number=f"IMP-{date.today().year}-001",
            status="pending",
            import_date=date.today(),
            created_by=self.user
        )

    def test_import_item_creation(self):
        item = ImportItem.objects.create(
            import_record=self.import_obj,
            product=self.product,
            expected_quantity=5
        )
        self.assertEqual(item.received_quantity, 0)
        self.assertEqual(str(item), f"Test Product - IMP-{date.today().year}-001")

    def test_received_quantity_validation(self):
        item = ImportItem.objects.create(
            import_record=self.import_obj,
            product=self.product,
            expected_quantity=5
        )
        with self.assertRaises(ValidationError):
            item.received_quantity = 6
            item.save()

class ProductUnitTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Test Category")
        self.product = Product.objects.create(
            name="Test Product",
            category=self.category,
            description="Test Description",
            specifications={
                "potencia": 100,
                "peso": 5.5,
                "dimensiones": "30x20x10",
                "voltaje": 220,
                "frecuencia": 50
            }
        )
        self.user = User.objects.create_user(username="testuser")
        self.import_obj = Import.objects.create(
            reference_number=f"IMP-{date.today().year}-001",
            status="pending",
            import_date=date.today(),
            created_by=self.user
        )
        self.import_item = ImportItem.objects.create(
            import_record=self.import_obj,
            product=self.product,
            expected_quantity=2
        )

    def test_product_unit_creation(self):
        unit = ProductUnit.objects.create(
            product=self.product,
            import_item=self.import_item,
            serial_number="LPX1-2024-001",
            status="available"
        )
        self.assertEqual(str(unit), "Test Product - LPX1-2024-001")
        self.assertEqual(self.import_item.received_quantity, 1)

    def test_invalid_serial_number(self):
        with self.assertRaises(ValidationError):
            ProductUnit.objects.create(
                product=self.product,
                import_item=self.import_item,
                serial_number="INVALID-SERIAL",
                status="available"
            )

    def test_exceed_expected_quantity(self):
        # Create first unit
        ProductUnit.objects.create(
            product=self.product,
            import_item=self.import_item,
            serial_number="LPX1-2024-001",
            status="available"
        )
        # Create second unit
        ProductUnit.objects.create(
            product=self.product,
            import_item=self.import_item,
            serial_number="LPX1-2024-002",
            status="available"
        )
        # Try to create third unit (should fail)
        with self.assertRaises(ValidationError):
            ProductUnit.objects.create(
                product=self.product,
                import_item=self.import_item,
                serial_number="LPX1-2024-003",
                status="available"
            )

    def test_status_transition(self):
        unit = ProductUnit.objects.create(
            product=self.product,
            import_item=self.import_item,
            serial_number="LPX1-2024-001",
            status="available"
        )
        # Valid transition
        unit.status = "in_use"
        unit.save()
        self.assertEqual(unit.status, "in_use")

        # Invalid transition
        unit.status = "disposed"
        with self.assertRaises(ValidationError):
            unit.save()
