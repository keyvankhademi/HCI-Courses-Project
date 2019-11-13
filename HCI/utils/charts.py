import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

import pandas as pd
from collections import Counter

import json
import operator
import nltk
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
import gensim
from gensim.corpora import Dictionary
import re

from HCI.models import Course, University, Topic
from django.db.models import Prefetch

def generate_charts():
    x = [c.last_taught.year for c in Course.objects.all()]

    num_bins = 5
    n, bins, patches = plt.hist(x, num_bins, facecolor='blue', alpha=0.5)

    plt.ylabel('Number of Courses')
    plt.xlabel('Last Year Taught')
    plt.title('Number of Courses per Year')

    plt.savefig("word_cloud/year_hist.png")

    plt.cla()

    dic = {}
    for c in Course.objects.all():
        if c.university.name not in dic:
            dic[c.university.name] = 0
        dic[c.university.name] += 1
    data = [(key, val) for key, val in dic.items()]
    data = sorted(data, key=lambda x: -x[1])

    labels = [x[0] for x in data[:4]]
    sizes = [x[1] for x in data[:4]]

    labels.append('others')
    sizes.append(sum([x[1] for x in data[4:]]))

    patches, texts = plt.pie(sizes, shadow=True, startangle=90)
    plt.legend(patches, labels, loc="best")
    plt.axis('equal')
    plt.tight_layout()
    plt.savefig("word_cloud/uni_pie.png")

#frequency of syllabus years


def get_years():
    years = [course.last_taught.year for course in Course.objects.all()]
    df = pd.Series(years).value_counts(sort=False)
    data = {
        'title': "syllabus years histogram",
        'labels': df.keys().tolist(),
        'values': df.tolist()
    }

    return data

#frequency of terms


def get_terms_freq():
    desc = ", ".join(topic.description for topic in Topic.objects.all())

    punctuation = list(string.punctuation)
    stop = stopwords.words('english') + punctuation + ["The", "This"]
    lem = WordNetLemmatizer()

    count = Counter([lem.lemmatize(word).lower() for word in nltk.word_tokenize(desc)
                     if word not in stop])
    data = {
        'title': "terms histogram",
        'labels': [],
        'values': []
    }

    for x, y in count.most_common():
        data['labels'].append(x)
        data['values'].append(y)

    return data

def get_sent_freq():

    desc = ", ".join(topic.description for topic in Topic.objects.all())

    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    d = []
    desc = desc.lower()
    for sentence in tokenizer.tokenize(desc):
        d.extend(sentence.split(','))
    count = Counter(d)

    data = {
        'title': "sentence histogram",
        'labels': [],
        'values': []
    }

    for x, y in count.most_common(20):
        data['labels'].append(x)
        data['values'].append(y)

    return data


def geo_data():
    data = {
        'country density': [['Country', 'Number']],
        'university': [],
        'region density': [['State', 'Number']]
    }

    countries = [uni.country for uni in University.objects.all()
                 if len(uni.country) > 1]
    states = [uni.state for uni in University.objects.all()
              if len(uni.state) > 1]
    count_country = Counter(countries)
    count_state = Counter(states)

    for c, a in count_country.most_common():
        data['country density'].append([c, a])
    for c, a in count_state.most_common():
        data['region density'].append([c, a])

    return data


def compare_data():
    data = {
        'all': [['Word', 'Frequency']],
        'Canada': [['Word', 'Frequency']],
        'USA': [['Word', 'Frequency']]
    }

    all = ", ".join(topic.description for topic in Topic.objects.all())
    data['all'].extend(get_terms(all))

    cad_set = Topic.objects.prefetch_related(Prefetch(
        'course__university', queryset=University.objects.filter(country='Canada'), to_attr='country'))

    cad = ", ".join(
        topic.description for topic in cad_set.filter(country='Canada'))
    data['Canada'].extend(get_terms(cad))

    us_set = Topic.objects.prefetch_related(Prefetch(
        'course__university', queryset=University.objects.filter(country='United States'),to_attr='country'))

    us = ", ".join(
        topic.description for topic in us_set)
    data['USA'].extend(get_terms(us))
    
    return data


def get_terms(desc):
    punctuation = list(string.punctuation)
    stop = stopwords.words('english') + punctuation + ["The", "This", '"']
    lem = WordNetLemmatizer()

    count = Counter([lem.lemmatize(word.lower()) for word in nltk.word_tokenize(desc)
                     if word not in stop])

    data = []
    for x, y in count.most_common():
        data.append([x, y])

    return data
