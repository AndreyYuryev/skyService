from django.core.management import BaseCommand
from users.models import User
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    def handle(self, *args, **options):
        group_normal = Group.objects.create(name='normal1')
        view_permissions = Permission.objects.filter(codename__startswith='view_')
        group_normal.permissions.set(view_permissions)
        group_normal.save()

        # 25,
        # 26,
        # 27,
        # 28,
        # 41,
        # 42,
        # 43,
        # 44,
        # 29,
        # 30,
        # 31,
        # 32,
        # 33,
        # 34,
        # 35,
        # 36

        group_moderator = Group.objects.create(name='moderator1')
        perm_names =['view_client', 'view_message', "change_stream", "set_active", "set_client", "view_stream",]
        permissions = []
        for perm_name in perm_names:
            permission = Permission.objects.get(codename=perm_name)
            permissions.append(permission)
        group_moderator.permissions.set(permissions)
        group_moderator.save()
