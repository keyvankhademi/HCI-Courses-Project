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

from HCI.models import Course, University

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
    desc = " ".join(course.description for course in Course.objects.all())

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


#sentences frequency
def get_sent_freq():
    desc = "\n".join(course.description for course in Course.objects.all())

    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    d = []
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

