from django.shortcuts import render
from django.views.generic import ListView, DetailView
from blogstream.models import Article


# Create your views here.
class ArticleDetailView(DetailView):
    model = Article
    fields = '__all__'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset=queryset)
        self.object.viewed += 1
        self.object.save()
        return self.object


class ArticleListView(ListView):
    model = Article
