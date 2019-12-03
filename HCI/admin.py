from django.contrib import admin

# Register your models here.
from HCI.models import University, Course, Criteria, Topic


class UniversityAdmin(admin.ModelAdmin):
    pass


class TopicInlineAdmin(admin.TabularInline):
    model = Topic


class CriteriaInlineAdmin(admin.TabularInline):
    model = Criteria


class CourseAdmin(admin.ModelAdmin):
    inlines = [TopicInlineAdmin, CriteriaInlineAdmin]
    list_display = ['name', 'code', 'university', 'complete', 'verified']
    list_filter = ['complete', 'verified', 'university__name']
    search_fields = ['name', 'code']


class CriteriaAdmin(admin.ModelAdmin):
    pass


class TopicAdmin(admin.ModelAdmin):
    pass


admin.site.register(University, UniversityAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Criteria, CriteriaAdmin)
admin.site.register(Topic, TopicAdmin)
