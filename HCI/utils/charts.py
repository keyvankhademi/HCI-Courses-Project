import string
from collections import Counter

import matplotlib.pyplot as plt
import nltk
import pandas as pd
from nltk.corpus import stopwords, wordnet
from nltk.stem.wordnet import WordNetLemmatizer
import re
from HCI.models import Course, University, Topic

wordnet.ensure_loaded()


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


# frequency of syllabus years
def get_years():
    years = [course.last_taught.year for course in Course.objects.all()]
    df = pd.Series(years).value_counts(sort=False)
    data = {
        'title': "syllabus years histogram",
        'labels': df.keys().tolist(),
        'values': df.tolist()
    }

    return data


# frequency of terms
def get_terms_freq():
    desc = ", ".join(topic.description for topic in Topic.objects.all())
    desc += ", ".join(course.learning_goals for course in Course.objects.all())
    return get_terms(desc)


def get_sent_freq():
    desc = ", ".join(topic.description for topic in Topic.objects.all())
    desc += ", ".join(course.learning_goals for course in Course.objects.all())

    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    d = []
    desc = desc.lower()

    for sentence in tokenizer.tokenize(desc):
        for line in filter(None, re.split("[,.\n\r!?:\)(\"]+", sentence)):
            if (len(line) > 2):
                d.append(line.strip())
    count = Counter(d)

    data = {
        'title': "sentence histogram",
        'labels': [],
        'values': []
    }

    for x, y in count.most_common(200):
        data['labels'].append(x)
        data['values'].append(y)

    return data


def geo_data():
    data = {
        'country density': [['Country', 'Number']],
        'university': [],
        'region density': [['State', 'Number']]
    }

    countries = []
    for uni in University.objects.all():
        if len(uni.country) > 1:
            if uni.country == 'United States of America' or uni.country == "USA":
                countries.append('United States')
            else:
                countries.append(uni.country)
    states = [uni.state for uni in University.objects.all()
              if len(uni.state) > 1]
    count_country = Counter(countries)
    count_state = Counter(states)

    for c, a in count_country.most_common():
        if c == 'United States of America' or c == "USA":
            c = 'United States'
        data['country density'].append([c, a])
    for c, a in count_state.most_common():
        data['region density'].append([c, a])

    return data


def get_terms_ca():
    cad_set = Topic.objects.filter(
        course__university__country='Canada').select_related()
    cad = ", ".join(topic.description for topic in cad_set)
    return get_terms(cad)


def get_terms_us():
    us_set = Topic.objects.filter(
        course__university__country='United States').select_related()
    us = ", ".join(topic.description for topic in us_set)
    return get_terms(us)


def get_terms(desc):
    punctuation = list(string.punctuation)
    stop = stopwords.words('english') + punctuation + \
           ["The", "This", '"', "''", "'s"]

    lem = WordNetLemmatizer()

    count = Counter([lem.lemmatize(word.lower()) for word in nltk.word_tokenize(desc) if word not in stop])

    data = {'labels': [], 'values': []}
    for x, y in count.most_common():
        data['labels'].append(x)
        data['values'].append(y)

    return data
