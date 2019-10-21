import json
import matplotlib.pyplot as plt
import math
import operator
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
import gensim
from gensim.corpora import Dictionary


def load_data():
    """
    loads the data.json and return it as a dictionary
    :return: data as dictionary
    """
    file = open("data.json", "r")
    data = json.load(file)
    file.close()
    return data


def get_time_frequency(data=load_data()):
    """
    :param data: dictionary of all the data
    :return: a dictionary containing key: year and value: frequency
    """
    dates_counter = {}

    for course in data:
        # because of the formating some values are nan and that fucks with everything
        # So this kinda fix it
        if str(course["last_taught"]) == "nan" or str(course["last_taught"]) == "":
            course["last_taught"] = "unknown"

        if course["last_taught"] in dates_counter:
            dates_counter[str(course["last_taught"])] += 1
        else:
            dates_counter[str(course["last_taught"])] = 1

    # matplot to visualize if you want to
    # plt.bar(list(dates_counter.keys()), list(dates_counter.values()), width = 0.75)
    # plt.show()

    return dates_counter


def get_terms(data=load_data()):
    """

    :param data: dictionary of all the data
    :return: list of all terms
    """

    # things to ignore
    punctuation = list(string.punctuation)
    stop = stopwords.words('english') + punctuation
    lem = WordNetLemmatizer()

    # get all terms
    terms = []
    for sheet in data:
        for topic in sheet['topics']:
            # test for lda
            terms.extend([lem.lemmatize(word) for word in nltk.word_tokenize(
                topic["title"].lower()) if word not in stop])

    return terms


def count_terms(number=10):
    """
    :param number: number of the terms to return
    :return:  top common terms
    """

    terms = get_terms()
    counter = Counter(terms)

    return counter.most_common(number)


# lda not working properly
def get_topics(data=load_data()):
    terms = get_terms()
    dictionary = Dictionary([terms])
    term_matrix = [dictionary.doc2bow(topic) for topic in [terms]]

    lda = gensim.models.ldamodel.LdaModel
    ldamodel = lda(term_matrix, num_topics=2, id2word=dictionary)

    print(ldamodel.print_topics())


# ------------------test---------------#
print(get_time_frequency())
# count_terms()
# get_topics()
