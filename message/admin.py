from django.contrib import admin

# Register your models here.
from message.models import Message


class MessageAdmin(admin.ModelAdmin):
    pass


admin.site.register(Message, MessageAdmin)
