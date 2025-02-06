from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.product import ProductViewSet
from .views.import import ImportViewSet
from .views.category import CategoryViewSet
from .views.import_item import ImportItemViewSet
from .views.product_unit import ProductUnitViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'imports', ImportViewSet)
router.register(r'import-items', ImportItemViewSet)
router.register(r'product-units', ProductUnitViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
