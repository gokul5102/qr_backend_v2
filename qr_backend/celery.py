from __future__ import absolute_import,unicode_literals
import os
from celery import Celery
from django.apps import apps 
from django.conf import settings
from celery.schedules import crontab
# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qr_backend.settings')

app = Celery('qr_backend')

app.conf.enable_utc=False
app.conf.update(timezone='Asia/Kolkata')


# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'db-replication-every-day-at-1-am': {
        'task': 'attendance_marker.tasks.replicate_database',
        'schedule': crontab(hour=1, minute=10),
        #'args': (2,)
    }
    
}

# Load task modules from all registered Django apps.
app.config_from_object(settings)
app.autodiscover_tasks(lambda: [n.name for n in apps.get_app_configs()])


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')