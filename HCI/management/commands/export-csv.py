import csv
import os
from datetime import datetime

from django.core.management.base import BaseCommand

from HCI.models import Course


class Command(BaseCommand):
    def handle(self, *args, **options):
        url = os.path.join("export-csv", datetime.now().strftime("%Y-%m-%d %H-%M-%S"))
        os.mkdir(url)
        f = open(os.path.join(url, "courses.csv"), "w", encoding="UTF-8", newline='\n')

        fnames = ['id', 'slug', 'name', 'code', 'university', 'description', 'url', 'prerequisites', 'core_for_major',
                  'last_taught', 'instructor', 'learning_goals', 'criteria', 'topics', ]

        writer = csv.DictWriter(f, fieldnames=fnames)
        writer.writeheader()
        for course in Course.objects.all():
            writer.writerow({
                'id': course.pk,
                "slug": course.slug,
                "name": course.name,
                "code": course.code,
                "university": course.university.name,
                "description": course.description,
                "url": course.url,
                "prerequisites": course.prerequisites,
                "core_for_major": course.core_for_major,
                "last_taught": course.last_taught.strftime("%m/%d/%Y, %H:%M:%S"),
                "instructor": course.instructor,
                "learning_goals": course.learning_goals,
                "criteria": ";".join([c.name + ": " + str(c.weight) for c in course.criteria_set.all()]),
                "topics": ";".join([str(t.week) + ": " + t.description for t in course.topic_set.all()])
            })
        f.close()
