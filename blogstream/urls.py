from django.urls import path
from blogstream.apps import BlogstreamConfig

app_name = BlogstreamConfig.name

urlpatterns = [
    path('', StartView.as_view(), name='start'),
]
