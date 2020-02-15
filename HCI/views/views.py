from django.shortcuts import render


# Create your views here.
from HCI.models import Course
from charts.views import get_criteria_chart_data_dict


def homepage(request):

    courses = Course.objects.all()[:4]

    sample_data_chart_data_dict = get_criteria_chart_data_dict()

    return render(request, "homepage.html", {
        'courses': courses,
        'sample_chart_labels': sample_data_chart_data_dict['labels'],
        'sample_chart_data': sample_data_chart_data_dict['data'],
    })
