from message.models import Message


def send_message(sender, receiver, text):
    message = Message()
    message.sender = sender
    message.receiver = receiver
    message.message = text
    message.save()
