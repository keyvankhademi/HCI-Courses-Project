"""HCI_Course URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

from HCI import views
from django.contrib.auth import views as auth_views

from HCI.views import signup_view, UniversityCreateView, CourseCreateView, UserProfileView, generate_word_cloud_view, generate_charts_view, get_year_hist, get_terms_freq, get_sent_freq, geo_data, compare_data

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/signup/', signup_view, name='signup'),
    path('accounts/profile/', UserProfileView.as_view(), name='profile'),
    path('accounts/change-password/', auth_views.PasswordChangeView.as_view(template_name='password_change.html'),
         name="password_change"),
    path('account/password-change-done/', TemplateView.as_view(template_name='password_change_done.html'),
         name="password_change_done"),
    path('add/university/', UniversityCreateView.as_view(), name='add_university'),
    path('add/course/', CourseCreateView.as_view(), name='add_course'),

    path('word-cloud/', TemplateView.as_view(template_name='word_cloud.html'), name='word_cloud'),
    path('word-cloud/generate', generate_word_cloud_view, name='generate_word_cloud'),

    path('charts/', TemplateView.as_view(template_name='charts.html'), name='charts'),
    path('charts/generate', generate_charts_view, name='generate_charts'),
    path('charts/years/frequency/', get_year_hist, name='year_hist'),
    path('charts/terms/frequency/', get_terms_freq, name='terms_hist'),
    path('charts/sentences/frequency/', get_sent_freq, name='sent_hist'),

    path('charts/geodata/', geo_data, name='geo_data'),
    path('charts/compare/', compare_data, name='compare_data'),

    path('', views.homepage, name='homepage'),
]
