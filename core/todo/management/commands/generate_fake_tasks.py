from django.core.management.base import BaseCommand
from faker import Faker
from accounts.models import User
from todo.models import Task
import random

class Command(BaseCommand):
    help = "inserting dummy data"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker()


    def handle(self, *args, **options):
        user, created = User.objects.get_or_create(email=self.fake.email(), password="test@123456")
        
        if created:
            user.set_password("test@123456")
            user.save()

        for _ in range(5):
            Task.objects.create(
                user = user,
                title = self.fake.paragraph(nb_sentences=1),
                complete = random.choice([True, False]),
            )