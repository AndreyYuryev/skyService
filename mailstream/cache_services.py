from django.conf import settings
from django.core.cache import cache
from mailstream.models import Client


def get_clients():
    clients = None
    if settings.CACHE_ENABLED:
        key = f'all_clients'
        clients = cache.get(key)
        if clients is None:
            clients = Client.objects.all()
            cache.set(key, clients)
    else:
        clients = Client.objects.all()
    return clients
