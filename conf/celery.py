import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf.settings')
celery_app = Celery('conf')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks()
celery_app.conf.timezone = "Europe/Moscow"

celery_app.conf.beat_schedule = {
    'add-each_day_of_a_new-month': {
        'task': 'apps.tele_cod.tasks.start_bot',
        'schedule': crontab(0, 12, day_of_month='1'),
    },
}
