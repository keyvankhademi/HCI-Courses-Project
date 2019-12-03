from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Message(models.Model):
    sender = models.ForeignKey(User, verbose_name="Sender User", on_delete=models.SET_NULL, null=True, db_index=True,
                               related_name='send_messages')
    receiver = models.ForeignKey(User, verbose_name="Receiver User", on_delete=models.CASCADE, null=False,
                                 db_index=True, related_name='received_messages')

    message = models.TextField(verbose_name="The message text")

    read = models.BooleanField(default=False, db_index=True)
