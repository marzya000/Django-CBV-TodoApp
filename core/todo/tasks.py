from celery import shared_task
from .models import Task


@shared_task
def clean_done_tasks():
    Task.objects.filter(complete=True).delete()
    print("done tasks are deleted")
