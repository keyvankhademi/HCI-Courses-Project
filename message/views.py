# Create your views here.
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView

from message.models import Message


class MessageListView(ListView):
    model = Message
    template_name = 'message/message_list_view.html'

    def get_queryset(self):
        return Message.objects.filter(receiver=self.request.user, read=False).order_by('-pk')


class MessageDetailView(UserPassesTestMixin, ListView):
    model = Message
    template_name = 'message/message_detail_view.html'

    def get_message(self):
        message_id = self.request.GET.get('message', None)
        return get_object_or_404(Message, pk=message_id)

    def test_func(self):
        return self.request.user == self.get_message().receiver

    def get_queryset(self):
        message = self.get_message()
        result = []
        while message is not None:
            message.read_message()
            result.append(message)
            message = message.reply_to
        return result


def message_delete_view(request):
    message = get_object_or_404(Message, pk=request.GET.get('message', None))

    if message.receiver != request.user:
        raise Http404

    message.delete()

    return render(request, 'message.html', {
        'title': 'Message Deleted',
        'message': "Message deleted successfully",
    })
