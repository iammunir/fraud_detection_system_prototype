from celery import Celery
from app.settings import Config

celery_app = Celery('fraud_detection',
                    broker=Config.CELERY_BROKER,
                    backend=Config.CELERY_BACKEND)

celery_app.conf.update(
    task_routes={
        'app.tasks.preprocess_transaction': {'queue': 'preprocessing'},
        'app.tasks.predict_transaction': {'queue': 'prediction'},
        'app.tasks.store_transaction': {'queue': 'storage'},
        'app.tasks.monitor_transaction': {'queue': 'monitor'}
    },
    task_track_started=True
)

celery_app.autodiscover_tasks(['app'])
