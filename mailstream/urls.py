from django.urls import path
from mailstream.apps import MailstreamConfig
from mailstream.views import StartView, MessageCreateView, MessageDetailView, MessageUpdateView, ClientCreateView, \
    ClientUpdateView, ClientDetailView, MaillistCreateView, MaillistUpdateView, MaillistDetailView, StreamDetailView, \
    StreamCreateView

app_name = MailstreamConfig.name

urlpatterns = [
    path('', StartView.as_view(), name='start'),
    path('message/create/', MessageCreateView.as_view(), name='message_create'),
    path('message/detail/<int:pk>', MessageDetailView.as_view(), name='message_detail'),
    path('message/edit/<int:pk>', MessageUpdateView.as_view(), name='message_edit'),

    path('client/create/', ClientCreateView.as_view(), name='client_create'),
    path('client/edit/<int:pk>', ClientUpdateView.as_view(), name='client_edit'),
    path('client/detail/<int:pk>', ClientDetailView.as_view(), name='client_detail'),

    path('maillist/create/', MaillistCreateView.as_view(), name='maillist_create'),
    path('maillist/edit/<int:pk>', MaillistUpdateView.as_view(), name='maillist_edit'),
    path('maillist/detail/<int:pk>', MaillistDetailView.as_view(), name='maillist_detail'),

    path('stream/create/', StreamCreateView.as_view(), name='stream_create'),
    path('stream/detail/<int:pk>', StreamDetailView.as_view(), name='stream_detail'),
]
