from django.core.management.base import BaseCommand
import json

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
                "equivalent": [{
                    "code": eq.code,
                    "university": eq.university.name,
                } for eq in course.equivalent.all()]
            })
        return data

    def get_criteria_data(self):
        data = []
        for criteria in Criteria.objects.all():
            data.append({
                "name": criteria.name,
                "weight": criteria.weight,
                "course": {
                    "code": criteria.course.code,
                    "university": criteria.course.university.name,
                }
            })
        return data

    def get_topic_data(self):
        data = []
        for topic in Topic.objects.all():
            data.append({
                "week": topic.week,
                "description": topic.description,
                "course": {
                    "code": topic.course.code,
                    "university": topic.course.university.name,
                },
            })
        return data

    def handle(self, *args, **options):
        self.export("export/university.json", self.get_university_data())
        self.export("export/courses.json", self.get_courses_data())
        self.export("export/criteria.json", self.get_criteria_data())
        self.export("export/topic.json", self.get_topic_data())

