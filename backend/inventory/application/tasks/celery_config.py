from celery.schedules import crontab

# Celery beat schedule configuration
CELERY_BEAT_SCHEDULE = {
    'check-low-stock': {
        'task': 'inventory.application.tasks.import_tasks.check_low_stock',
        'schedule': crontab(hour='*/1'),  # Run every hour
    },
    'generate-periodic-reports': {
        'task': 'inventory.application.tasks.import_tasks.generate_periodic_reports',
        'schedule': crontab(hour='0', minute='0'),  # Run daily at midnight
    },
}

# Task routing configuration
CELERY_TASK_ROUTES = {
    'inventory.application.tasks.import_tasks.*': {'queue': 'imports'},
}

# Task serialization configuration
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TIMEZONE = 'UTC'
CELERY_ENABLE_UTC = True

# Task execution settings
CELERY_TASK_TIME_LIMIT = 30 * 60  # 30 minutes
CELERY_TASK_SOFT_TIME_LIMIT = 25 * 60  # 25 minutes
CELERY_TASK_MAX_RETRIES = 3
CELERY_TASK_RETRY_DELAY = 60  # 1 minute

# Result backend settings
CELERY_RESULT_BACKEND = 'django-db'
CELERY_RESULT_EXTENDED = True
CELERY_RESULT_EXPIRES = 60 * 60 * 24  # 24 hours
