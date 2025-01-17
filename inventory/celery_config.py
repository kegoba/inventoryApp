from __future__ import absolute_import, unicode_literals
from celery import Celery
import os
from decouple import config


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory.settings')

app = Celery('inventory')


app.config_from_object('django.conf:settings', namespace='CELERY')

# Use RabbitMQ as the message broker
app.conf.update(
    broker_url= config("CELERY_BROKER_URL"),
    result_backend='rpc://',
)


app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
