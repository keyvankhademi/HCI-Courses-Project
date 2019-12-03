from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render
# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView

from message.utils import send_message
from report.models import CourseReport, UniversityReport


def report_success_view(request):
    return render(request, 'message.html', {
        'title': 'Your report has been sent successfully',
        'message': 'Thank you for helping',
    })


class CourseReportCreateView(UserPassesTestMixin, CreateView):
    def test_func(self):
        return self.request.user.is_authenticated

    model = CourseReport
    template_name = 'report/course_report.html'
    fields = ('course', 'reason', 'message')
    success_url = reverse_lazy('report:success')

    def form_valid(self, form):
        result = super().form_valid(form)
        course_report = self.object

        if self.request.user.is_authenticated and course_report.course.user is not None:
            send_message(self.request.user, course_report.course.user,
                         "One of your Courses has been report\nCourse: {}".format(course_report.course))
        return result


class UniversityReportCreateView(UserPassesTestMixin, CreateView):
    def test_func(self):
        return self.request.user.is_authenticated

    model = UniversityReport
    template_name = 'report/university_report.html'
    fields = ('university', 'reason', 'message')
    success_url = reverse_lazy('report:success')
