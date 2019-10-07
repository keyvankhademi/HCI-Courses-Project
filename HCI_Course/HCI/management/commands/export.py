from django.core.management.base import BaseCommand
import json
import os
from datetime import datetime

from HCI.models import University, Course, Criteria, Topic


class Command(BaseCommand):

    def export(self, file_name, data):
        f = open(file_name, "w")
        f.write(json.dumps(data))
        f.close()

    def get_university_data(self):
        data = []
        for uni in University.objects.all():
            data.append({
                "name": uni.name,
            })
        return data

    def get_courses_data(self):
        data = []
        for course in Course.objects.all():
            data.append({
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
                "equivalent": [eq.slug for eq in course.equivalent.all()]
            })
        return data

    def get_criteria_data(self):
        data = []
        for criteria in Criteria.objects.all():
            data.append({
                "name": criteria.name,
                "weight": criteria.weight,
                "course": criteria.course.slug,
            })
        return data

    def get_topic_data(self):
        data = []
        for topic in Topic.objects.all():
            data.append({
                "week": topic.week,
                "description": topic.description,
                "course": topic.course.slug,
            })
        return data

    def handle(self, *args, **options):

        url = os.path.join("export", datetime.now().strftime("%Y-%m-%d %H-%M-%S"))
        os.mkdir(url)

        self.export(os.path.join(url, "university.json"), self.get_university_data())
        self.export(os.path.join(url, "courses.json"), self.get_courses_data())
        self.export(os.path.join(url, "criteria.json"), self.get_criteria_data())
        self.export(os.path.join(url, "topic.json"), self.get_topic_data())

