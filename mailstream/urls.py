from django.urls import path
from mailstream.apps import MailstreamConfig
from mailstream.views import (StartView,
                              MessageCreateView, MessageDetailView, MessageUpdateView, MessageListView,
                              MessageDeleteView,
                              ClientCreateView, ClientUpdateView, ClientDetailView, ClientDeleteView, ClientListView,
                              StreamDetailView, StreamCreateView, StreamUpdateView, StreamDeleteView, StreamListView)

app_name = MailstreamConfig.name

urlpatterns = [
    path('', StartView.as_view(), name='start'),

    path('client/list/', ClientListView.as_view(), name='client_list'),
    path('client/create/', ClientCreateView.as_view(), name='client_create'),
    path('client/update/<int:pk>', ClientUpdateView.as_view(), name='client_update'),
    path('client/detail/<int:pk>', ClientDetailView.as_view(), name='client_detail'),
    path('client/delete/<int:pk>', ClientDeleteView.as_view(), name='client_delete'),

    path('message/list/', MessageListView.as_view(), name='message_list'),
    path('message/create/', MessageCreateView.as_view(), name='message_create'),
    path('message/detail/<int:pk>', MessageDetailView.as_view(), name='message_detail'),
    path('message/update/<int:pk>', MessageUpdateView.as_view(), name='message_update'),
    path('message/delete/<int:pk>', MessageDeleteView.as_view(), name='message_delete'),

    path('stream/list/', StreamListView.as_view(), name='stream_list'),
    path('stream/create/', StreamCreateView.as_view(), name='stream_create'),
    path('stream/detail/<int:pk>', StreamDetailView.as_view(), name='stream_detail'),
    path('stream/update/<int:pk>', StreamUpdateView.as_view(), name='stream_update'),
    path('stream/delete/<int:pk>', StreamDeleteView.as_view(), name='stream_delete'),
]
