from django.shortcuts import render, redirect
from django.views.generic import ListView, DeleteView, DetailView, CreateView, UpdateView, TemplateView
from django.urls import reverse_lazy
from mailstream.models import Message, Client, Stream
from mailstream.forms import DateForm
from mailstream.services import STATUS_VALUES, REGULARITY_VALUES
from django.forms import modelform_factory
from blogstream.models import Article
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Group
from users.models import User


class StartView(TemplateView):
    template_name = 'start.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Сервис рассылок'
        articles = Article.objects.all().order_by('-created_at').values()
        articles_list = []
        for item in range(3):
            articles_list.append(articles[item])
        context_data['articles_list'] = articles_list
        clients_count = Client.objects.all().count()
        context_data['clients'] = clients_count
        active_streams_count = Stream.objects.filter(is_active=True).count()
        context_data['active_streams'] = active_streams_count
        all_streams_count = Stream.objects.all().count()
        context_data['all_streams'] = all_streams_count
        return context_data


class ClientCreateView(PermissionRequiredMixin, CreateView):
    model = Client
    fields = ('fullname', 'email', 'comments',)
    extra_context = {'title': 'Создание подписчика', 'button': 'Добавить', 'header': 'Добавить подписчика'}
    permission_required = 'mailstream.add_client'

    def get_success_url(self):
        return reverse_lazy('mailstream:client_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        self.object = form.save()
        self.object.created_by = self.request.user
        self.object.save()
        return super().form_valid(form)


class ClientUpdateView(PermissionRequiredMixin, UpdateView):
    model = Client
    fields = ('comments',)
    extra_context = {'title': 'Изменение подписчика', 'button': 'Изменить', 'header': 'Изменить подписчика'}
    permission_required = 'mailstream.change_client'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['fullname'] = self.object.fullname
        context['email'] = self.object.email
        return context

    def get_success_url(self):
        return reverse_lazy('mailstream:client_detail', kwargs={'pk': self.object.pk})


class ClientDeleteView(PermissionRequiredMixin, DeleteView):
    model = Client
    extra_context = {'title': 'Удаление подписчика', 'button': 'Удаление'}
    success_url = reverse_lazy('mailstream:client_list')
    permission_required = 'mailstream.delete_client'


class ClientDetailView(PermissionRequiredMixin, DetailView):
    model = Client
    extra_context = {'title': 'Обзор подписчика'}
    permission_required = 'mailstream.view_client'


class ClientListView(PermissionRequiredMixin, ListView):
    model = Client
    extra_context = {'title': 'Обзор подписчиков'}
    permission_required = 'mailstream.view_client'

    def get_queryset(self, **kwargs):
        if self.request.user.groups.filter(name='moderator').exists():
            return Client.objects.all()
        return Client.objects.filter(created_by=self.request.user)


class MessageCreateView(PermissionRequiredMixin, CreateView):
    model = Message
    extra_context = {'title': 'Создание сообщения рассылки', 'button': 'Добавить'}
    fields = ('subject', 'body',)
    permission_required = 'mailstream.add_message'

    def get_success_url(self):
        return reverse_lazy('mailstream:message_detail', kwargs={'pk': self.object.pk})


class MessageUpdateView(PermissionRequiredMixin, UpdateView):
    model = Message
    fields = ('body',)
    permission_required = 'mailstream.change_message'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Изменение текста сообщения рассылки'
        context['button'] = 'Измененить'
        context['subject'] = self.object.subject
        return context

    def get_success_url(self):
        return reverse_lazy('mailstream:message_detail', kwargs={'pk': self.object.pk})


class MessageDeleteView(PermissionRequiredMixin, DeleteView):
    model = Message
    extra_context = {'title': 'Удаление текста сообщения рассылки', 'button': 'Удалить'}
    success_url = reverse_lazy('mailstream:message_list')
    permission_required = 'mailstream.delete_message'


class MessageDetailView(PermissionRequiredMixin, DetailView):
    model = Message
    extra_context = {'title': 'Обзор содержимого рассылки'}
    permission_required = 'mailstream.view_message'


class MessageListView(PermissionRequiredMixin, ListView):
    model = Message
    extra_context = {'title': 'Обзор текстов рассылок'}
    permission_required = 'mailstream.view_message'

    # def get_queryset(self, **kwargs):
    #     if self.request.user.groups.filter(name='moderator').exists():
    #         return Message.objects.all()
    #     return Message.objects.filter(created_by=self.request.user)


class StreamCreateView(PermissionRequiredMixin, CreateView):
    model = Stream
    form_class = DateForm
    extra_context = {'title': 'Создание настроек рассылки', 'button': 'Добавить'}
    permission_required = 'mailstream.add_stream'

    def get_success_url(self):
        return reverse_lazy('mailstream:stream_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        self.object = form.save()
        self.object.created_by = self.request.user
        self.object.save()
        return super().form_valid(form)

    # def get_form_class(self):
    #     return modelform_factory(form=DateForm, model=Stream,
    #                              fields='__all__')


class StreamUpdateView(PermissionRequiredMixin, UpdateView):
    model = Stream
    form_class = DateForm
    extra_context = {'title': 'Изменение настроек рассылки', 'button': 'Изменить'}
    permission_required = 'mailstream.change_stream'

    def get_success_url(self):
        return reverse_lazy('mailstream:stream_list')

    def get_form_class(self):
        return modelform_factory(form=DateForm, model=Stream,
                                 fields=['client', 'is_active', ])

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['extra_value'] = self.object
        context['regularity_list'] = REGULARITY_VALUES
        return context


class StreamDeleteView(PermissionRequiredMixin, DeleteView):
    model = Stream
    extra_context = {'title': 'Удаление рассылки', 'button': 'Удаление'}
    success_url = reverse_lazy('mailstream:stream_list')
    permission_required = 'mailstream.delete_stream'


class StreamDetailView(PermissionRequiredMixin, DetailView):
    model = Stream
    permission_required = 'mailstream.view_stream'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Обзор настроек рассылки'
        context['status_list'] = STATUS_VALUES
        context['regularity_list'] = REGULARITY_VALUES
        return context


class StreamListView(PermissionRequiredMixin, ListView):
    model = Stream
    permission_required = 'mailstream.view_stream'

    def get_queryset(self, **kwargs):
        is_active = self.request.GET.get('active', '')
        if self.request.user.groups.filter(name='moderator').exists():
            if is_active:
                return Stream.objects.filter(is_active=True)
            else:
                return Stream.objects.all()
        else:
            if is_active:
                return Stream.objects.filter(is_active=True, created_by=self.request.user)
            else:
                return Stream.objects.filter(created_by=self.request.user)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Обзор рассылок'
        context['status_list'] = STATUS_VALUES
        context['regularity_list'] = REGULARITY_VALUES
        return context
