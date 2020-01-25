from dal import autocomplete
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Q
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, DetailView, UpdateView

from HCI.choices import get_all_states, ALL_STATES
from HCI.forms import CourseCreateForm, UniversityCreateForm, CourseFilterForm
from HCI.models import University, Course


@method_decorator(login_required, name='dispatch')
class UniversityCreateView(CreateView):
    model = University
    template_name = 'models/university_create.html'
    success_url = reverse_lazy('university:add')
    form_class = UniversityCreateForm

    def form_valid(self, form):
        response = super(UniversityCreateView, self).form_valid(form)

        self.object.user = self.request.user
        self.object.save()

        return response


@method_decorator(login_required, name='dispatch')
class CourseCreateView(CreateView):
    model = Course
    template_name = 'models/course_create.html'
    success_url = reverse_lazy('course:add')
    form_class = CourseCreateForm

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
        query = self.request.GET.get('query', None)
        county = self.request.GET.get('country', None)
        university = self.request.GET.get('university', None)

        q = Q()

        if my_courses:
            user = self.request.user
            q = q & Q(user=user)

        if query:
            q = q & (Q(name__contains=query) | Q(code__contains=query))

        if county and county != 'ALL':
            q = q & Q(university__country=county)

        if university:
            q = q & Q(university=university)

        return Course.objects.filter(q).all()

    def get_context_data(self, **kwargs):
        context = super(CourseListView, self).get_context_data(**kwargs)
        object_list = context['object_list']

        for object in object_list:
            object.editable = True if object.user == self.request.user else False

        context['form'] = CourseFilterForm(self.request.GET)

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


class UniversityAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = University.objects.all()
        if self.q:
            qs = qs.filter(name__contains=self.q)
        return qs


class CourseEquivalentAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Course.objects.all()
        if self.q:
            qs = qs.filter(name__contains=self.q)
        return qs


class StateAutoComplete(autocomplete.Select2ListView):

    def get_list(self):
        country = self.forwarded.get('country', None)
        if not country or country not in ALL_STATES:
            return []
        return ALL_STATES[country].items()

    def autocomplete_results(self, results):
        token = self.q or ""
        return [(x, y) for (x, y) in results if token.lower() in (x + y).lower()]

    def results(self, results):
        """Return the result dictionary."""
        return [dict(id=x[0], text=x[1]) for x in results]
