from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, DetailView, UpdateView

from HCI.models import University, Course


@method_decorator(permission_required('HCI.add_university'), name='dispatch')
class UniversityCreateView(CreateView):
    model = University
    template_name = 'models/university_create.html'
    success_url = reverse_lazy('university:add')
    fields = ['name', 'short_name']

    def form_valid(self, form):
        response = super(UniversityCreateView, self).form_valid(form)

        self.object.user = self.request.user
        self.object.save()

        return response


@method_decorator(permission_required('HCI.add_course'), name='dispatch')
class CourseCreateView(CreateView):
    model = Course
    template_name = 'models/course_create.html'
    success_url = reverse_lazy('course:add')
    fields = ['name', 'code', 'university', 'description', 'url', 'prerequisites', 'core_for_major',
              'last_taught', 'instructor', 'learning_goals', 'equivalent']

    def form_valid(self, form):
        response = super(CourseCreateView, self).form_valid(form)

        self.object.user = self.request.user
        self.object.save()

        return response


class CourseListView(ListView):
    model = Course
    template_name = 'models/course_list_view.html'

    def get_queryset(self):
        my_courses = self.request.GET.get('my_courses', None)

        if my_courses:
            user = self.request.user
            if not user.is_authenticated:
                return []
            return Course.objects.filter(user=user).all()
        else:
            return Course.objects.all()

    def get_context_data(self, **kwargs):
        context = super(CourseListView, self).get_context_data(**kwargs)
        object_list = context['object_list']

        for object in object_list:
            object.editable = True if object.user == self.request.user else False

        return context


class CourseDetailView(DetailView):
    model = Course
    template_name = 'models/course_detail_view.html'

    def get_context_data(self, **kwargs):
        context = super(CourseDetailView, self).get_context_data(**kwargs)

        object = context['object']
        object.editable = True if object.user == self.request.user else False

        return context


class CourseUpdateView(UserPassesTestMixin, UpdateView):

    def test_func(self):
        return self.get_object().user == self.request.user

    model = Course
    template_name = 'models/course_update.html'
    fields = ['name', 'code', 'university', 'description', 'category', 'url', 'prerequisites', 'core_for_major',
              'last_taught', 'instructor', 'learning_goals', 'equivalent']

    def get_success_url(self):
        return reverse('course:detail_view', None, [self.kwargs.get('pk'), ])


class UniversityListView(ListView):
    model = University
    template_name = 'models/university_list_view.html'


class UniversityDetailView(DetailView):
    model = University
    template_name = 'models/university_detail_view.html'


class UniversityUpdateView(UpdateView):
    model = University
    template_name = 'models/university_update.html'
    fields = ['name', 'short_name']

    def get_success_url(self):
        return reverse('university:detail_view', None, [self.kwargs.get('pk'), ])
