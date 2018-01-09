#!/bin/python
#-*- coding:utf-8 -*-
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery,platforms
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nekodashboard.settings')
app = Celery('nekodashboard')
platforms.C_FORCE_ROOT = True
from django.conf import settings
from datetime import timedelta
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj.settings')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.update(
    CELERYBEAT_SCHEDULE = {
        'do-task-every-30-seconds': {
            'task': 'containers.tasks.All_Host',
            'schedule': timedelta(seconds=7),
        },
    },
)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))  # dumps its own request information