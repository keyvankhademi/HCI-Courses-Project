from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render


# Create your views here.
from HCI.models import Course, Criteria
from HCI.utils import charts
from HCI.utils.word_cloud import generate_word_cloud


def criteria_chart_view(request):

    courses = Course.objects.all()

    project_count = 0
    final_exam_count = 0
    both_count = 0

    for course in courses:
        project = False
        final_exam = False
        for criteria in course.criteria_set.all():
            if 'project' in criteria.name.lower():
                project = True
            if 'final' in criteria.name.lower() and 'project' not in criteria.name.lower():
                final_exam = True
        if project and not final_exam:
            project_count += 1
        if final_exam and not project:
            final_exam_count += 1
        if project and final_exam:
            both_count += 1

    return render(request, 'charts/criteria_charts.html', {
        'labels': ["Project", "Final Exam", "Both"],
        'data': [project_count, final_exam_count, both_count],
    })


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