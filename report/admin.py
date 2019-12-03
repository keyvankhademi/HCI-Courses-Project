from django.contrib import admin

# Register your models here.
from report.models import UniversityReport, CourseReport


class UniversityReportAdmin(admin.ModelAdmin):
    pass


class CourseReportAdmin(admin.ModelAdmin):
    pass


admin.site.register(UniversityReport, UniversityReportAdmin)
admin.site.register(CourseReport, CourseReportAdmin)
