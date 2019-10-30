from django.core.management.base import BaseCommand
import json
import os
from datetime import datetime

from HCI.models import University, Course, Criteria, Topic


class Command(BaseCommand):

    import_files = ['university.json', 'courses.json', 'criteria.json', 'topic.json']

    def add_arguments(self, parser):
        parser.add_argument('-url', help="Url of the folder containing json files")

    def find_latest_export(self):
        url = os.path.join(".", "export")

        if not os.path.exists(url):
            raise FileNotFoundError

        folders = [x[0] for x in os.walk(url)]

        if len(folders) < 2:
            raise FileNotFoundError

        folders = sorted(folders, reverse=True)

        return folders[0]

    def read_file(self, path):
        f = open(path, "r")
        return json.loads(f.read())

    def import_universities(self, data):
        for datum in data:
            uni = University()
            uni.name = datum['name']
            uni.short_name = datum['short_name']
            uni.country = datum['country']
            uni.state = datum['state']
            uni.city = datum['city']

            uni.save()

    def import_courses(self, data):
        for datum in data:
            course = Course()
            course.slug = datum['slug']
            course.name = datum['name']
            course.code = datum['code']
            course.university = University.objects.get(name=datum['university'])
            course.description = datum['description']
            course.url = datum['url']
            course.prerequisites = datum['prerequisites']
            course.core_for_major = datum['core_for_major']
            course.last_taught = datetime.strptime(datum['last_taught'], "%m/%d/%Y, %H:%M:%S")
            course.instructor = datum['instructor']
            course.learning_goals = datum['learning_goals']

            course.save()

        for datum in data:
            course = Course.objects.get(slug=datum['slug'])
            course.equivalent.set(Course.objects.filter(slug__in=datum['equivalent']))

    def import_topics(self, data):
        for datum in data:
            topic = Topic()
            topic.week = datum['week']
            topic.description = datum['description']
            topic.course = Course.objects.get(slug=datum['course'])

            topic.save()

    def import_criteria(self, data):
        for datum in data:
            criteria = Criteria()
            criteria.name = datum['name']
            criteria.weight = datum['weight']
            criteria.course = Course.objects.get(slug=datum['course'])

            criteria.save()

    def handle(self, *args, **options):

        url = options['url']
        if url is None:
            try:
                url = self.find_latest_export()
            except FileNotFoundError:
                self.stdout.write("Cannot find latest export file please specify url using -url.")
                return

        dir = os.path.normpath(url)

        for f in Command.import_files:
            if f not in os.listdir(dir):
                self.stdout.write("Cannot find " + f + " in the given directory")
                return

        self.stdout.write("Importing from " + dir + ". This will result in deleting existing database. continue?[y/N]")
        answer = input()
        if answer[0].lower() != 'y':
            self.stdout.write("Import aborted.")
            return

        University.objects.all().delete()
        Course.objects.all().delete()
        Topic.objects.all().delete()
        Criteria.objects.all().delete()

        self.import_universities(self.read_file(os.path.join(dir, "university.json")))
        self.import_courses(self.read_file(os.path.join(dir, "courses.json")))
        self.import_topics(self.read_file(os.path.join(dir, "topic.json")))
        self.import_criteria(self.read_file(os.path.join(dir, "criteria.json")))

