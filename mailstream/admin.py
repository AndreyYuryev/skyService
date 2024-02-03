from django.contrib import admin
from mailstream.models import Client, Stream, Message, Log


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'email','comments', 'created_by')
    list_filter = ('fullname', 'email',)
    search_fields = ('fullname',)


@admin.register(Stream)
class StreamAdmin(admin.ModelAdmin):
    list_display = ('name', 'regularity', 'status', 'started_at', 'ended_at', 'created_by', 'is_active',)
    list_filter = ('name', 'regularity', 'status',)
    search_fields = ('name',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'body',)
    list_filter = ('subject',)
    search_fields = ('subject',)


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('stream', 'client', 'attempt_status', 'last_attempt',)
    list_filter = ('stream', 'client', 'attempt_status',)
    search_fields = ('stream', 'client', 'attempt_status',)

