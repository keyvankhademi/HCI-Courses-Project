from django.db.models import Q
from django.shortcuts import render


# Create your views here.
from HCI.models import Course, Criteria


def criteria_chart_view(request):

    project = Criteria.objects.filter(Q(name__contains='Project') | Q(name__contains='project'))
    final_exam = Criteria.objects.filter(Q(name__contains='final') | Q(name__contains='Final'))
    both = project.intersection(final_exam)

    return render(request, 'charts/criteria_charts.html', {
        'labels': ["Project", "Final Exam", "Both"],
        'data': [project.count(), final_exam.count(), both.count()],
    })
