from celery import Celery

celery_app = Celery(
    'app',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0',
    include=['app.tasks']
)

celery_app.conf.update(
    result_expires=3600,
    broker_connection_retry_on_startup=True  
)
