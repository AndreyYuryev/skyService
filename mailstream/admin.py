from django.contrib import admin
from models import Client, Stream


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'email',)
    list_filter = ('fullname', 'email',)
    search_fields = ('fullname',)


@admin.register(Stream)
class StreamAdmin(admin.ModelAdmin):
    list_display = ('regularity', 'status', 'post_time',)
    list_filter = ('regularity', 'status',)
    search_fields = ('regularity', 'status', )