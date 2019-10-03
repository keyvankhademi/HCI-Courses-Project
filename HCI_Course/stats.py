import json
import matplotlib.pyplot as plt
import math

import operator
import json
from collections import Counter
from nltk.corpus import stopwords
import string

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
        if str(course["last_taught"]) == "nan" or str(course["last_taught"]) == "":
            course["last_taught"] = "unknown"

        if course["last_taught"] in dates_counter:
            dates_counter[str(course["last_taught"])] += 1
        else:
            dates_counter[str(course["last_taught"])] = 1

    #plt.bar(list(dates_counter.keys()), list(dates_counter.values()), width = 0.75)
    #plt.show()

    return dates_counter

#todo
def get_topics():
    return
    """
    counter = Counter()

    punctuation = list(string.punctuation)
    stop = stopwords.words('english') + punctuation + ['rt', 'via']

    file = open("HCI_Course\course_list.xlsx", "r")
    data = json.load(file)

    for topics in data['topics']:
     break

    file.close() 
      

    #print(counter.most_common(10))
    """
    

get_time_frequency()