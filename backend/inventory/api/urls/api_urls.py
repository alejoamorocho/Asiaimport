from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ..views.product_viewset import ProductViewSet
from ..views.import_viewset import ImportViewSet
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'imports', ImportViewSet, basename='import')

urlpatterns = [
    # API base URLs
    path('', include(router.urls)),
    
    # Authentication URLs
    path('auth/', include('rest_framework.urls')),
    
    # API Documentation URLs
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path(
        'docs/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui'
    ),
    path(
        'redoc/',
        SpectacularRedocView.as_view(url_name='schema'),
        name='redoc'
    ),
]
