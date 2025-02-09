"""
Configuration settings for the inventory domain.
These settings can be overridden in the Django settings file.
"""

from typing import Dict, Any
from django.conf import settings

# Default configuration
DEFAULT_CONFIG: Dict[str, Any] = {
    # Product settings
    'PRODUCT_DEFAULT_STOCK_THRESHOLD': 10,
    'PRODUCT_SKU_PREFIX': '',
    'PRODUCT_SKU_LENGTH': 8,
    
    # Import settings
    'IMPORT_BATCH_SIZE': 100,
    'IMPORT_MAX_ITEMS': 1000,
    'IMPORT_ALLOWED_STATUSES': [
        'pending',
        'processing',
        'completed',
        'failed'
    ],
    
    # Cache settings
    'CACHE_TIMEOUT': 3600,  # 1 hour
    'CACHE_PREFIX': 'inventory:',
    
    # Notification settings
    'NOTIFICATION_ENABLED': True,
    'NOTIFICATION_CHANNELS': ['email', 'slack'],
    'NOTIFICATION_EMAIL_FROM': 'inventory@example.com',
    'NOTIFICATION_SLACK_CHANNEL': '#inventory-alerts',
    
    # Report settings
    'REPORT_DEFAULT_DAYS': 30,
    'REPORT_CACHE_TIMEOUT': 3600,  # 1 hour
}

# Get configuration from Django settings
INVENTORY_CONFIG = getattr(settings, 'INVENTORY_CONFIG', {})

# Merge default config with user config
CONFIG = {**DEFAULT_CONFIG, **INVENTORY_CONFIG}

# Export individual settings
PRODUCT_DEFAULT_STOCK_THRESHOLD = CONFIG['PRODUCT_DEFAULT_STOCK_THRESHOLD']
PRODUCT_SKU_PREFIX = CONFIG['PRODUCT_SKU_PREFIX']
PRODUCT_SKU_LENGTH = CONFIG['PRODUCT_SKU_LENGTH']

IMPORT_BATCH_SIZE = CONFIG['IMPORT_BATCH_SIZE']
IMPORT_MAX_ITEMS = CONFIG['IMPORT_MAX_ITEMS']
IMPORT_ALLOWED_STATUSES = CONFIG['IMPORT_ALLOWED_STATUSES']

CACHE_TIMEOUT = CONFIG['CACHE_TIMEOUT']
CACHE_PREFIX = CONFIG['CACHE_PREFIX']

NOTIFICATION_ENABLED = CONFIG['NOTIFICATION_ENABLED']
NOTIFICATION_CHANNELS = CONFIG['NOTIFICATION_CHANNELS']
NOTIFICATION_EMAIL_FROM = CONFIG['NOTIFICATION_EMAIL_FROM']
NOTIFICATION_SLACK_CHANNEL = CONFIG['NOTIFICATION_SLACK_CHANNEL']

REPORT_DEFAULT_DAYS = CONFIG['REPORT_DEFAULT_DAYS']
REPORT_CACHE_TIMEOUT = CONFIG['REPORT_CACHE_TIMEOUT']
