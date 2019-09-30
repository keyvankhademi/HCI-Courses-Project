from django.core.management.base import BaseCommand
import json

from HCI.models import University


class Command(BaseCommand):

    def export(self, file_name, data):
        f = open(file_name, "w")
        f.write(json.dumps(data))
        f.close()

    def get_university_data(self):
        data = []
        for uni in University.objects.all():
            print(uni)
            data.append({
                "name": uni.name,
            })
        return data

    def handle(self, *args, **options):
        self.export("export/university.json", self.get_university_data())

