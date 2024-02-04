# Generated by Django 5.0.1 on 2024-02-03 15:21

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailstream', '0005_stream_is_active_alter_stream_client'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='stream',
            name='start_time',
            field=models.TimeField(default=django.utils.timezone.now, verbose_name='Время рассылки'),
        ),
        migrations.AlterField(
            model_name='client',
            name='comments',
            field=models.TextField(blank=True, null=True, verbose_name='Комментарии'),
        ),
        migrations.AlterField(
            model_name='client',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='message',
            name='body',
            field=models.TextField(blank=True, null=True, verbose_name='Содержимое письма'),
        ),
        migrations.AlterField(
            model_name='message',
            name='subject',
            field=models.CharField(max_length=120, verbose_name='Тема письма'),
        ),
    ]
