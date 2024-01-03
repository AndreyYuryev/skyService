from django.contrib import admin
from models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'email',)
    list_filter = ('fullname', 'email',)
    search_fields = ('fullname',)
