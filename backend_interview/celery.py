import os
from datetime import timedelta

from backend_interview import settings
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend_interview.settings")
app = Celery("backend_interview")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.timezone = settings.TIME_ZONE
app.conf.beat_schedule = {
    "send_restock_and_sales_notification": {
        "task": "user_management.tasks.send_restock_and_sales_notification",
        "schedule": timedelta(hours=0, minutes=0),  # Run daily at midnight
    },
}
app.autodiscover_tasks()
