from django.urls import path
from blogstream.apps import BlogstreamConfig
from blogstream.views import ArticleListView, ArticleDetailView
from django.views.decorators.cache import cache_page

app_name = BlogstreamConfig.name

urlpatterns = [
    path('article/list', cache_page(60)(ArticleListView.as_view()), name='article_list'),
    path('article/detail/<int:pk>', ArticleDetailView.as_view(), name='article_detail'),
]
