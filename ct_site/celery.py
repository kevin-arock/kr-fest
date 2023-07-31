from __future__ import absolute_import, unicode_literals
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE' , 'ct_site.settings')
from celery import Celery
from django.conf import settings
from celery.schedules import crontab
from post.tasks import send_mail_task


os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')
app = Celery('ct_site')
app.config_from_object('django.conf:settings' , namespace='CELERY')

app.conf.enable_utc=False
app.conf.update(timezone='Asia/Kolkata')
# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
# Load task modules from all registered Django apps.
# Celery Beat tasks registration
app.conf.beat_schedule = {
'Send_mail_to_Client': {
'task': 'post.tasks.send_mail_task',
'schedule': 30.0, #every 30 seconds it will be called
#'args': (2,) you can pass arguments also if rquired
}
}
app.autodiscover_tasks()
@app.task(bind=True)
def debug_task(self):
	print(f'Request: {self.request!r}')

