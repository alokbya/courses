#!/usr/bin/env python

import pandas as pd
from course import *
url = "http://catalog.oregonstate.edu/CourseDetail.aspx?Columns=afghijklmnopqrstuvwyz{&SubjectCode=ME&CourseNumber=498&Term=201802"
tables = pd.read_html(url, header=0)
#print(tables[5])
#print('Columns: ' + str(len(tables[5].columns)))
# info = scrape_course()
# print(info)
print('Length of Table: ' + str(len(tables)))
for i in range(len(tables)):
    try:
        if len(tables[i].columns) == 22:
            print('22!')
            print(i)
    except:
        print('doesnt work')
# df = pd.DataFrame(info)
# print(df)