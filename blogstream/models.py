from django.db import models
from mailstream.services import NULLABLE


# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текс статьи', **NULLABLE)
    image = models.ImageField(upload_to='articles/', verbose_name='Изображение', **NULLABLE)
    viewed = models.IntegerField(default=0, verbose_name='Просмотры')
    created_at = models.DateField(auto_now_add=True, verbose_name='Создано')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-created_at']
