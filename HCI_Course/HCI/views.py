from boto.connection import HTTPRequest
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect


# Create your views here.
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView

from HCI.models import University, Course


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
