from django.core.management.base import BaseCommand
import string
import numpy as np
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt

from HCI.models import University, Course, Criteria, Topic


class Command(BaseCommand):
    def handle(self, *args, **options):
        text = " ".join(course.description for course in Course.objects.all())
        text = text.translate({ord(key): None for key in string.punctuation})

        wordcloud = WordCloud(background_color='white', width=900, height=600, max_words=50).generate(text)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()

        wordcloud.to_file("word_cloud/wc.png")
