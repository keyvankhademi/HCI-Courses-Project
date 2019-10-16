from HCI.models import University, Course, Criteria, Topic
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


#frequency of syllabus years
def get_years():
    years = [course.last_taught.year for course in Course.objects.all()]
    df = pd.Series(years).value_counts()
    data = {
        'title': "syllabus years histogram",
        'labels': df.keys().tolist(),
        'values': df.tolist()
    }

    return data


def get_terms_freq():
    desc = " ".join(course.description for course in Course.objects.all())
   
    punctuation = list(string.punctuation)
    stop = stopwords.words('english') + punctuation + ["The","This"]
    lem = WordNetLemmatizer()

    count = Counter([lem.lemmatize(word).lower() for word in nltk.word_tokenize(desc)
                     if word not in stop])
    data = {
        'title': "terms histogram",
        'labels': [],
        'values': []
    }

    for x,y in count.most_common():
        data['labels'].append(x)
        data['values'].append(y)

    return data
