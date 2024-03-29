# Generated by Django 5.0.1 on 2024-02-01 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Заголовок')),
                ('text', models.TextField(blank=True, null=True, verbose_name='Текс статьи')),
                ('image', models.ImageField(blank=True, null=True, upload_to='article/', verbose_name='Изображение')),
                ('viewed', models.IntegerField(default=0, verbose_name='Просмотры')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='Создано')),
            ],
            options={
                'verbose_name': 'Статья',
                'verbose_name_plural': 'Статьи',
            },
        ),
    ]
