import csv

import random

import re


import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

with open('enews.csv', encoding="UTF-8") as file:

    reader = csv.reader(file)

    next(reader)

    readers = list(reader)
    print(readers[1])

    # count = 0
    mylist = []
    for row in readers:
        title = (row[2] + "" + row[1])
        # print(title)
        mylist.append(title)
    # print(mylist)


    # stopwords from NLTK
    my_stopwords = nltk.corpus.stopwords.words('english')

    # add the new custom stopwords to my stopwords
    my_stopwords.extend(mylist)


    myList = [re.sub(r'[^a-zA-Z]',' ',string) for string in mylist]

    x = random.choice(myList)
    print(x)
    y = x.lower()
    print(y)










