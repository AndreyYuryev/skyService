from django.contrib import admin
from blogstream.models import Article


# Register your models here.
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'image', 'viewed', 'created_at',)
    list_filter = ('title',)
    search_fields = ('titele', 'text',)
