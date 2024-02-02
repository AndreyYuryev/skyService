from django.shortcuts import render, redirect
from django.views.generic import ListView, DeleteView, DetailView, CreateView, UpdateView, TemplateView
from django.urls import reverse_lazy
from mailstream.models import Message, Client, Stream
from mailstream.forms import DateForm
from mailstream.services import STATUS_VALUES
from django.forms import modelform_factory

# Create your views here.
class StartView(TemplateView):
    template_name = 'start.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Сервис рассылок'
        return context_data


class ClientCreateView(CreateView):
    model = Client
    fields = ('fullname', 'email', 'comments',)
    extra_context = {'title': 'Создание подписчика', 'button': 'Добавить'}

    def get_success_url(self):
        return reverse_lazy('mailstream:client_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        self.object = form.save()
        self.object.created_by = self.request.user
        self.object.save()
        return super().form_valid(form)


class ClientUpdateView(UpdateView):
    model = Client
    fields = ('fullname', 'email', 'comments',)
    extra_context = {'title': 'Изменение подписчика', 'button': 'Изменить'}

    def get_success_url(self):
        return reverse_lazy('mailstream:client_detail', kwargs={'pk': self.object.pk})


class ClientDetailView(DetailView):
    model = Client
    extra_context = {'title': 'Обзор подписчика'}


class ClientDeleteView(DeleteView):
    model = Client
    extra_context = {'title': 'Удаление подписчика', 'button': 'Удаление'}


class ClientListView(ListView):
    model = Client
    extra_context = {'title': 'Обзор подписчиков'}


class MessageCreateView(CreateView):
    model = Message
    extra_context = {'title': 'Создание сообщения рассылки', 'button': 'Добавить'}
    fields = ('subject', 'body',)

    def get_success_url(self):
        return reverse_lazy('mailstream:message_detail', kwargs={'pk': self.object.pk})


class MessageUpdateView(UpdateView):
    model = Message
    fields = ('body',)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Изменение текста сообщения рассылки'
        context['button'] = 'Измененить'
        context['subject'] = self.object.subject
        return context


class MessageDetailView(DetailView):
    model = Message
    extra_context = {'title': 'Обзор содержимого рассылки'}


class StreamCreateView(CreateView):
    model = Stream
    form_class = DateForm
    extra_context = {'title': 'Создание настроек рассылки', 'button': 'Добавить'}

    def get_success_url(self):
        return reverse_lazy('mailstream:stream_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        self.object = form.save()
        self.object.created_by = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_form_class(self):
        return modelform_factory(form=DateForm, model=Stream,
                                 fields='__all__')


class StreamDetailView(DetailView):
    model = Stream
    extra_context = {'title': 'Обзор настроек рассылки'}


class StreamUpdateView(UpdateView):
    model = Stream
    form_class = DateForm
    extra_context = {'title': 'Изменение настроек рассылки', 'button': 'Изменить'}

    def get_success_url(self):
        return reverse_lazy('mailstream:stream_list')

    def get_form_class(self):
        return modelform_factory(form=DateForm, model=Stream,
                                 fields=['client', 'is_active',])

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['extra_value'] = self.object.name
        return context

class StreamDeleteView(DeleteView):
    model = Stream
    extra_context = {'title': 'Удаление рассылки', 'button': 'Удаление'}


class StreamListView(ListView):
    model = Stream

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Обзор рассылок'
        context['status_list'] = STATUS_VALUES
        return context
