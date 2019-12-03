from django.urls import path

from report.views import CourseReportCreateView, UniversityReportCreateView, report_success_view

urlpatterns = [
    path('course/', CourseReportCreateView.as_view(), name='course'),
    path('university/', UniversityReportCreateView.as_view(), name='university'),
    path('success/', report_success_view, name='success'),
]
