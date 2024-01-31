from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from django.urls import reverse_lazy
from mailstream.models import Message, Client, MailList, Stream
from mailstream.models import REGULARITY_VALUES as regularity, STATUS_VALUES as status_values
from mailstream.forms import DateTimeForm


# Create your views here.
class StartView(TemplateView):
    template_name = 'start.html'


class MessageCreateView(CreateView):
    model = Message
    extra_context = {'title': 'Создание сообщения рассылки'}
    fields = ('subject', 'body',)

    def get_success_url(self):
        return reverse_lazy('mailstream:message_detail', kwargs={'pk': self.object.pk})


class MessageUpdateView(UpdateView):
    model = Message
    fields = ('body',)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Изменение сообщения рассылки'
        context['subject'] = self.object.subject
        return context


class MessageDetailView(DetailView):
    model = Message


class ClientCreateView(CreateView):
    model = Client
    # extra_context = {'title': 'Создание клиента'}
    fields = ('fullname', 'email', 'comments',)

    def get_success_url(self):
        return reverse_lazy('mailstream:client_detail', kwargs={'pk': self.object.pk})


class ClientUpdateView(UpdateView):
    model = Client
    fields = ('fullname', 'email', 'comments',)
    extra_context = {'title': 'Изменение клиента'}

    def get_success_url(self):
        return reverse_lazy('mailstream:client_detail', kwargs={'pk': self.object.pk})


class ClientDetailView(DetailView):
    model = Client


class MaillistCreateView(CreateView):
    model = MailList
    # extra_context = {'title': 'Создание клиента'}
    fields = ('stream', 'client',)

    def get_success_url(self):
        return reverse_lazy('mailstream:maillist_detail', kwargs={'pk': self.object.pk})


class MaillistUpdateView(UpdateView):
    model = MailList
    fields = ('stream', 'client',)
    extra_context = {'title': 'Изменение получателей'}

    def get_success_url(self):
        return reverse_lazy('mailstream:maillist_detail', kwargs={'pk': self.object.pk})


class MaillistDetailView(DetailView):
    model = MailList


class StreamCreateView(CreateView):
    model = Stream
    form_class = DateTimeForm
    # fields = ('name',
    #           'started_at',
    #           'ended_at',
    #           'message',
    #           'regularity',
    #           'status',
    #           'all_recipient',)

    def get_success_url(self):
        return reverse_lazy('mailstream:stream_detail', kwargs={'pk': self.object.pk})


class StreamDetailView(DetailView):
    model = Stream
