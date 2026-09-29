from celery import Celery
from app import celery, send_email_task, send_scheduled_email

# This file ensures Celery can find tasks
# Tasks are already defined in app.py with @celery.task decorator