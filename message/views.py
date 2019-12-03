# Create your views here.
from django.views.generic import ListView

from message.models import Message


class MessageListView(ListView):
    model = Message
    template_name = 'message/message_list_view.html'

    def get_queryset(self):
        return Message.objects.filter(receiver=self.request.user, read=False).all()
