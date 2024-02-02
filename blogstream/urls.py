from django.urls import path
from blogstream.apps import BlogstreamConfig
from blogstream.views import ArticleListView, ArticleDetailView

app_name = BlogstreamConfig.name

urlpatterns = [
    path('article/list', ArticleListView.as_view(), name='article_list'),
    path('article/detail/<int:pk>', ArticleDetailView.as_view(), name='article_detail'),
]
