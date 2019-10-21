import string
import numpy as np
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt

from HCI.models import University, Course, Criteria, Topic


def generate_word_cloud():
    text = " ".join(course.description for course in Course.objects.all())
    text = text.translate({ord(key): None for key in string.punctuation})

    wordcloud = WordCloud().generate(text)
    wordcloud.to_file("word_cloud/wc.png")

    text = " ".join(course.learning_goals for course in Course.objects.all())
    text = text.translate({ord(key): None for key in string.punctuation})

    wordcloud = WordCloud().generate(text)
    wordcloud.to_file("word_cloud/wc_lg.png")

