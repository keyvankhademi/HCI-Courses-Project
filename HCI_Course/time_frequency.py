import json
import matplotlib.pyplot as plt
import math

def time_frequency(data):   
    dates_counter = {}
    for course in data:

        if course["last_taught"] in dates_counter:
            dates_counter[str(course["last_taught"])] += 1
        else:
            dates_counter[str(course["last_taught"])] = 1

    for key, value in dates_counter.items():
        print("{}: {}".format(key,value))

    plt.bar(list(dates_counter.keys()), list(dates_counter.values()), width = 0.75)
    plt.show()

    return


file = open("data.json","r")
data = json.load(file)

time_frequency(data)

file.close()

