#!/usr/bin/env python

import pandas as pd

url = "http://catalog.oregonstate.edu/CourseDetail.aspx?Columns=afghijklmnopqrstuvwyz{&SubjectCode=ME&CourseNumber=451&Term=201901"
tables = tables = pd.read_html(url, header=0)
print(tables[4])

calls_df, = pd.read_html(url, header=0)

print(calls_df.to_json(orient="records", date_format="iso"))
