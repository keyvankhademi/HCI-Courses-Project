import json
import matplotlib.pyplot as plt
import math

import operator
import json
from collections import Counter
from nltk.corpus import stopwords
import nltk
import string

#may have to download both
#nltk.download('stopwords')
#nltk.download('punkt')

def load_data():
    file = open("data.json", "r")
    data = json.load(file)
    file.close()
    return data

#returns a dictionary with 
#   key: year, 
#   value: frequency
def get_time_frequency(data = load_data()):   
    dates_counter = {}

    for course in data:
        #because of the formating some values are nan and that fucks with everything
        # So this kinda fix it
        if str(course["last_taught"]) == "nan" or str(course["last_taught"]) == "":
            course["last_taught"] = "unknown"

        if course["last_taught"] in dates_counter:
            dates_counter[str(course["last_taught"])] += 1
        else:
            dates_counter[str(course["last_taught"])] = 1

    #matplot to visualize if you want
    #plt.bar(list(dates_counter.keys()), list(dates_counter.values()), width = 0.75)
    #plt.show()

    return dates_counter

#gets the most used expressions
def get_terms(data = load_data(),number = 10):
    counter = Counter()

    punctuation = list(string.punctuation)
    stop = stopwords.words('english') + punctuation + ['rt', 'via']

    for topics in data:
        for topic in topics['topics']:
            counter.update(
                [word for word in nltk.word_tokenize(topic["title"].lower()) if word not in stop]
            )

    print(counter.most_common(number))
    return counter.most_common(number)
    

#get_time_frequency()
get_terms()

