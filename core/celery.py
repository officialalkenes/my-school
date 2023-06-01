from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.base")

app = Celery("core")

app.conf.enable_utc = False

app.conf.update(timezone="Africa/Lagos")

app.config_from_object(settings, namespace="CELERY")

# CELERY_BEAT_SETTINGS
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request {self.request!r}")
