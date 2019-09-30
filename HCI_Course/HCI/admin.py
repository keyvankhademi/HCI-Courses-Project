from django.contrib import admin

# Register your models here.
from HCI.models import University, Course, Criteria, Topic


class UniversityAdmin(admin.ModelAdmin):
    pass


class CourseAdmin(admin.ModelAdmin):
    pass


class CriteriaAdmin(admin.ModelAdmin):
    pass


class TopicAdmin(admin.ModelAdmin):
    pass


admin.site.register(University, UniversityAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Criteria, CriteriaAdmin)
admin.site.register(Topic, TopicAdmin)