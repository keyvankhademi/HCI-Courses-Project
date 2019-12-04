from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render, get_object_or_404
# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView

from HCI.models import Course, University
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

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        course_id = self.request.GET.get('course', None)
        if not course_id:
            return kwargs
        course = get_object_or_404(Course, pk=course_id)
        kwargs['initial'].update({
            'course': course,
        })

        return kwargs

    def form_valid(self, form):
        result = super().form_valid(form)
        course_report = self.object

        if self.request.user.is_authenticated and course_report.course.user is not None:
            send_message(self.request.user, course_report.course.user,
                         "One of your Courses has been reported\nCourse: {}".format(course_report.course))
        return result


class UniversityReportCreateView(UserPassesTestMixin, CreateView):
    def test_func(self):
        return self.request.user.is_authenticated

    model = UniversityReport
    template_name = 'report/university_report.html'
    fields = ('university', 'reason', 'message')
    success_url = reverse_lazy('report:success')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        university_id = self.request.GET.get('university', None)
        if not university_id:
            return kwargs
        university = get_object_or_404(University, pk=university_id)
        kwargs['initial'].update({
            'university': university,
        })
        return kwargs
