from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api.views.product import ProductViewSet
from .api.views.imports import ImportViewSet
from .api.views.category import CategoryViewSet
from .api.views.import_item import ImportItemViewSet
from .api.views.product_unit import ProductUnitViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'imports', ImportViewSet)
router.register(r'import-items', ImportItemViewSet)
router.register(r'product-units', ProductUnitViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
