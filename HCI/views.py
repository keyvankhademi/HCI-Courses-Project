from django.contrib.auth import login
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
# Create your views here.
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views.generic import CreateView, UpdateView, ListView, DetailView

from HCI.forms import SignupForm
from HCI.models import University, Course
from HCI.utils import charts
from HCI.utils.email_functions import send_email, account_activation_token
from HCI.utils.word_cloud import generate_word_cloud


def homepage(request):
    return render(request, "base.html")


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            send_email(request, user)
            return render(request, 'message.html', {
                'title': "Sign Up Successful",
                'message': "Thank you for signing up. An activation link is sent to your email. Please Activate your "
                           "account using that link",
            })
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


@method_decorator(permission_required('HCI.add_university'), name='dispatch')
class UniversityCreateView(CreateView):
    model = University
    template_name = 'university_create.html'
    success_url = reverse_lazy('add_university')
    fields = ['name', 'short_name']

    def form_valid(self, form):
        response = super(UniversityCreateView, self).form_valid(form)

        self.object.user = self.request.user
        self.object.save()

        return response


@method_decorator(permission_required('HCI.add_course'), name='dispatch')
class CourseCreateView(CreateView):
    model = Course
    template_name = 'course_create.html'
    success_url = reverse_lazy('add_course')
    fields = ['name', 'code', 'university', 'description', 'url', 'prerequisites', 'core_for_major',
              'last_taught', 'instructor', 'learning_goals', 'equivalent']

    def form_valid(self, form):
        response = super(CourseCreateView, self).form_valid(form)

        self.object.user = self.request.user
        self.object.save()

        return response


class UserProfileView(UpdateView):
    model = User
    template_name = 'profile.html'
    success_url = reverse_lazy('profile')
    fields = ['username', 'first_name', 'last_name', 'email']

    def get_object(self, queryset=None):
        return self.request.user


def generate_word_cloud_view(request):
    generate_word_cloud()
    return HttpResponse(status=200)


def generate_charts_view(request):
    charts.generate_charts()
    return HttpResponse(status=200)

def get_year_hist(request):
        data = charts.get_years()
        return JsonResponse(data)


def get_terms_freq(request):
    data = charts.get_terms_freq()
    return JsonResponse(data)


def get_sent_freq(request):
    data = charts.get_sent_freq()
    return JsonResponse(data)

def geo_data(request):
    data = charts.geo_data()
    return JsonResponse(data)

def get_terms_ca(request):
    data = charts.get_terms_ca()
    return JsonResponse(data)

def get_terms_us(request):
    data = charts.get_terms_us()
    return JsonResponse(data)

class CourseListView(ListView):
    model = Course
    template_name = 'course_list_view.html'

    def get_queryset(self):
        my_courses = self.request.GET.get('my_courses', None)

        if my_courses:
            user = self.request.user
            if not user.is_authenticated:
                return None
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
    template_name = 'course_detail_view.html'

    def get_context_data(self, **kwargs):
        context = super(CourseDetailView, self).get_context_data(**kwargs)

        object = context['object']
        object.editable = True if object.user == self.request.user else False

        return context


class CourseUpdateView(UserPassesTestMixin, UpdateView):

    def test_func(self):
        return self.get_object().user == self.request.user

    model = Course
    template_name = 'course_update.html'
    fields = ['name', 'code', 'university', 'description', 'category', 'url', 'prerequisites', 'core_for_major',
              'last_taught', 'instructor', 'learning_goals', 'equivalent']

    def get_success_url(self):
        return reverse('course_detail_view', None, [self.kwargs.get('pk'), ])


class UniversityListView(ListView):
    model = University
    template_name = 'university_list_view.html'


class UniversityDetailView(DetailView):
    model = University
    template_name = 'university_detail_view.html'


class UniversityUpdateView(UpdateView):
    model = University
    template_name = 'university_update.html'
    fields = ['name', 'short_name']

    def get_success_url(self):
        return reverse('university_detail_view', None, [self.kwargs.get('pk'), ])


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return render(request, 'message.html', {
            'title': "Your Account is Activated",
            'message': 'Thank you for your email confirmation. Now you can login your account.',
        })
    else:
        return render(request, 'message.html', {
            'title': "Something went wrong",
            'message': 'Activation link is invalid!',
        })
