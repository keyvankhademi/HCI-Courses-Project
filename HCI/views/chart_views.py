from django.http import HttpResponse, JsonResponse

from HCI.utils import charts
from HCI.utils.word_cloud import generate_word_cloud


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
