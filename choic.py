import csv
import random

import pandas as pd
from random import randrange
from random import randint

with open('enews.csv', encoding="UTF-8") as file:

    reader = csv.reader(file)

    next(reader)

    readers = list(reader)
    print(readers[1])

    # count = 0
    mylist = []
    for row in readers:
        title = (row[2] + "" + row[1])
        print(title)
        mylist.append(title)
    print(mylist)






    #
    #     if count > 5:
    #         break
    #
    #     count += 1
