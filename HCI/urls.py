from django.contrib.auth import views as auth_views
from django.urls import path, re_path
from django.views.generic import TemplateView

from HCI.views.account_views import *
from HCI.views.chart_views import *
from HCI.views.model_views import *

account_url_patterns = ([
    path('login/', auth_views.LoginView.as_view(template_name='account/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', signup_view, name='signup'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('change-password/', PasswordChangeView2.as_view(), name="password_change"),
    path('password-change-done/', password_change_done_view, name="password_change_done"),
    re_path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
         activate, name='activate'),
], 'account')

university_url_patterns = ([
    path('add', UniversityCreateView.as_view(), name='add'),
    path('list-view', UniversityListView.as_view(), name='list_view'),
    path('<int:pk>/', UniversityDetailView.as_view(), name='detail_view'),
    path('<int:pk>/update', UniversityUpdateView.as_view(), name='update'),
], 'university')

course_url_patterns = ([
    path('add', CourseCreateView.as_view(), name='add'),
    path('list-view', CourseListView.as_view(), name='list_view'),
    path('<int:pk>/', CourseDetailView.as_view(), name='detail_view'),
    path('<int:pk>/update', CourseUpdateView.as_view(), name='update'),
], 'course')

charts_url_patterns = ([
    path('word-cloud/', TemplateView.as_view(template_name='charts/word_cloud.html'), name='word_cloud'),
    path('word-cloud/generate', generate_word_cloud_view, name='generate_word_cloud'),

    path('', TemplateView.as_view(template_name='charts/charts.html'), name='charts'),
    path('generate', generate_charts_view, name='generate_charts'),
    path('years/frequency/', get_year_hist, name='year_hist'),
    path('terms/frequency/', get_terms_freq, name='terms_hist'),
    path('/sentences/frequency/', get_sent_freq, name='sent_hist'),

    path('geodata/', geo_data, name='geo_data'),
    path('terms/canada/', get_terms_ca, name='get_terms_ca'),
    path('terms/us/', get_terms_us, name='get_terms_us'),
], 'charts')
