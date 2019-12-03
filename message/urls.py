from django.urls import path

from message.views import MessageListView

urlpatterns = [
    path('list-view', MessageListView.as_view(), name='list_view')
]
