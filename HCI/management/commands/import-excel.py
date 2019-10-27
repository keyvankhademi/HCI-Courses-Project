import datetime

from django.core.management.base import BaseCommand
import json

from HCI.models import University, Course, Criteria, Topic


class Command(BaseCommand):

    def to_float(self, n):
        try:
            return float(n)
        except:
            return None

    def to_int(self, n):
        try:
            return int(n)
        except:
            return None

    def load_to_db(self, data):
        course = Course()
        name = data['name']
        course.name = name
        course.code = name

        course.university = University.objects.get()
        course.description = data['description']

        url = data['url']
        course.url = url if type(url) == str else None

        course.core_for_major = data['core_for_major']

        # TODO: fix this to actually calculate last taught
        course.last_taught = datetime.datetime.now()

        course.instructor = data['instructor']
        course.learning_goals = data['learning_goals']
        course.save()

        for cdata in data['criteria']:
            weight = self.to_float(cdata['weight'])
            if weight is None or weight != weight:
                continue

            # print(weight)

            criteria = Criteria()
            criteria.name = cdata['name']
            criteria.weight = weight
            criteria.course = course
            criteria.save()

        for tdata in data['topics']:

            if tdata['week'] != tdata['week']:
                continue

            week = self.to_int(tdata['week'].split()[1])
            if week is None or week != week:
                continue

            topic = Topic()
            topic.week = week
            topic.description = tdata['title']
            topic.course = course
            topic.save()

    def import_from_json(self, data):
        University.objects.all().delete()
        Course.objects.all().delete()
        Criteria.objects.all().delete()
        Topic.objects.all().delete()

        uni = University()
        uni.name = "Unknown"
        uni.save()

        for datum in data:
            self.load_to_db(datum)

    def handle(self, *args, **options):
        f = open("data.json", "r")
        js = f.read()
        data = json.loads(js)
        f.close()

        self.import_from_json(data)
