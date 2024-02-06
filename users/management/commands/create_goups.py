from django.core.management import BaseCommand
from users.models import User
from django.contrib.auth.models import Group
from django.core.management import call_command

class Command(BaseCommand):
    def handle(self, *args, **options):
        # group_normal = Group.objects.create()
        # Создание fixtures
        call_command('dumpdata', '--natural-foreign', '--exclude', 'auth.permission', '--exclude', 'contenttypes',
                     '--output', 'fixtures.json')