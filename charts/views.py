from django.db.models import Q
from django.shortcuts import render


# Create your views here.
from HCI.models import Course, Criteria


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
            if 'final' in criteria.name.lower():
                final_exam = True
        if project:
            project_count += 1
        if final_exam:
            final_exam_count += 1
        if project and final_exam:
            both_count += 1

    return render(request, 'charts/criteria_charts.html', {
        'labels': ["Project", "Final Exam", "Both"],
        'data': [project_count, final_exam_count, both_count],
    })
