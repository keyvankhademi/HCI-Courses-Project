from django.contrib import admin

# Register your models here.
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin


class MyUserAdmin(UserAdmin):
    model = get_user_model()


admin.site.register(get_user_model(), MyUserAdmin)
