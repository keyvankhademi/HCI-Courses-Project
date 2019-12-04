from django.urls import path

from message.views import MessageListView, MessageDetailView, message_delete_view

urlpatterns = [
    path('list-view', MessageListView.as_view(), name='list_view'),
    path('', MessageDetailView.as_view(), name='detail'),
    path('delete', message_delete_view, name='delete'),
]
