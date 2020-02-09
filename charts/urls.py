from django.urls import path
from django.views.generic import TemplateView

from charts.views import criteria_chart_view, generate_word_cloud_view, generate_charts_view, get_year_hist, \
    get_terms_freq, get_sent_freq, geo_data, get_terms_ca, get_terms_us

urlpatterns = [
    path('criteria', criteria_chart_view, name='criteria'),

    path('word-cloud/', TemplateView.as_view(template_name='charts/word_cloud.html'), name='word_cloud'),
    path('word-cloud/generate', generate_word_cloud_view, name='generate_word_cloud'),

    path('', TemplateView.as_view(template_name='charts/charts.html'), name='charts'),
    path('generate', generate_charts_view, name='generate_charts'),
    path('years/frequency/', get_year_hist, name='year_hist'),
    path('terms/frequency/', get_terms_freq, name='terms_hist'),
    path('sentences/frequency/', get_sent_freq, name='sent_hist'),

    path('geodata/', geo_data, name='geo_data'),
    path('terms/canada/', get_terms_ca, name='get_terms_ca'),
    path('terms/us/', get_terms_us, name='get_terms_us'),
]
