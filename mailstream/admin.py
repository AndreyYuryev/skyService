from django.contrib import admin
from mailstream.models import Client, Stream, Message, Log


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'email',)
    list_filter = ('fullname', 'email',)
    search_fields = ('fullname',)


@admin.register(Stream)
class StreamAdmin(admin.ModelAdmin):
    list_display = ('regularity', 'status', 'post_time',)
    list_filter = ('regularity', 'status',)
    search_fields = ('regularity', 'status',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'body',)
    list_filter = ('subject',)
    search_fields = ('subject',)


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('attempt_status', 'last_attempt',)
    list_filter = ('attempt_status',)
    search_fields = ('attempt_status',)
