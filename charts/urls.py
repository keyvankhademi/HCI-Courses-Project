from django.urls import path

from charts.views import criteria_chart_view

urlpatterns = [
    path('criteria', criteria_chart_view, name='criteria'),
]
