from django.core.management.base import BaseCommand
from os import path
from HCI.models import University, Course, Criteria, Topic
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt


class Command(BaseCommand):
    def handle(self, *args, **options):
        years = [course.last_taught.year for course in Course.objects.all()]
        print(type(pd.Series(years).value_counts()))
        pd.Series(years).value_counts().plot('bar')
        plt.show()
        
        
