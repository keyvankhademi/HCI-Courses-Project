from django.urls import path

from HCI.views.model_views import *

university_url_patterns = [
    path('add', UniversityCreateView.as_view(), name='add'),
    path('list-view', UniversityListView.as_view(), name='list_view'),
    path('<int:pk>/', UniversityDetailView.as_view(), name='detail_view'),
    path('<int:pk>/update', UniversityUpdateView.as_view(), name='update'),
    path('auto-complete', UniversityAutoComplete.as_view(), name='auto_complete'),
    path('state-auto-complete', StateAutoComplete.as_view(), name='state_auto_complete'),
]

course_url_patterns = [
    path('add', CourseCreateView.as_view(), name='add'),
    path('list-view', CourseListView.as_view(), name='list_view'),
    path('<int:pk>/', CourseDetailView.as_view(), name='detail_view'),
    path('<int:pk>/update', CourseUpdateView.as_view(), name='update'),
    path('auto-complete', CourseEquivalentAutoComplete.as_view(), name='auto_complete')
]
