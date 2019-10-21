import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

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
