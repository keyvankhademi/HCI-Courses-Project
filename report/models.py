from django.db import models

# Create your models here.
from HCI.models import Course, University

REPORT_REASONS = (
    ("Spam", "It's a spam"),
    ("Outdated", "Some fields need to be updated/filled"),
    ("Duplicated", "This is duplicated"),
)


class AbstractReport(models.Model):
    reason = models.CharField(max_length=100, choices=REPORT_REASONS)
    message = models.TextField(blank=True)


class CourseReport(AbstractReport):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reports')


class UniversityReport(AbstractReport):
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='reports')
