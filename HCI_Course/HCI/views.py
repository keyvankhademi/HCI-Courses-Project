from boto.connection import HTTPRequest
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect


# Create your views here.
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView

from HCI.models import University, Course
from HCI.utils import charts
from HCI.utils.word_cloud import generate_word_cloud






def homepage(request):
    return render(request, "base.html")


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('homepage')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


@method_decorator(permission_required('HCI.add_university'), name='dispatch')
class UniversityCreateView(CreateView):
    model = University
    template_name = 'university_create.html'
    success_url = reverse_lazy('add_university')
    fields = ['name', 'short_name']


@method_decorator(permission_required('HCI.add_course'), name='dispatch')
class CourseCreateView(CreateView):
    model = Course
    template_name = 'course_create.html'
    success_url = reverse_lazy('add_course')
    fields = ['name', 'code', 'university', 'description', 'url', 'prerequisites', 'core_for_major',
              'last_taught', 'instructor', 'learning_goals', 'equivalent']


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
