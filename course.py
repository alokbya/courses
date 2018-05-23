#!/usr/bin/env python
# Sources:
# 1. https://www.crummy.com/software/BeautifulSoup/bs4/doc/


from bs4 import BeautifulSoup
import urllib
import pandas as pd
import requests
import json
from omit_labs import omit


url = "http://catalog.oregonstate.edu/CourseDetail.aspx?Columns=afghijklmnopqrstuvwyz{&SubjectCode=ME&CourseNumber=451&Term=202000"

def to_url(ts):
    # properly generate the course url
    # this mainly handles the odd term dates used on the website

    terms = {
        'su': '00',
        'f': '01',
        'w': '02',
        'sp': '03'
    }

    year = int(ts[-2:])
    term = ts[:-2].lower()
    
    if term == 'su' or term == 'f':
        year+=1
    
    return '20' + str(year) + terms[term]
    
def get_data(url):
    f = urllib.request.urlopen(url)             # Fetch DOM at url
    soup = BeautifulSoup(f, "lxml")
    nt = pd.read_html(url, header=0)            # get number of tables

    # find the table with 22 columns (contains course data)
    table_num = 0                               # holds the table number with 22 columns
    class_bit = False                           # false unless there are classes offered for specified term
    for i in range(len(nt)):
        try:
            if len(nt[i].columns) == 22:
                table_num = i
                class_bit = True
        except:
            pass
    if class_bit:
        table = soup.find_all('table')[table_num]   # Table with class information
        df = pd.read_html(str(table))               # Create pandas dataframe with html table               
        raw_list = df[0].to_json(orient='records')  # Get data in JSON format
        d = json.loads(raw_list)                    # Convert raw_list to JSON object
        head = [d[0][(str(i))] for i in range(len(d[0]))]
        return d, soup, head
    return False

def get_class_name(soup):
    class_title = soup.h3.contents[2].strip().split('\n')
    title = [i.strip() for i in class_title]                # e.g. ['ME 311', 'INTRODUCTION TO THERMAL-FLUID SCIENCES', '(4).']
    class_name = str(title[0] + ': ' + title[1]).replace('.', '')
    return class_name

def get_dict(d, head):
    info = {}
    class_info = {}     # place holder
    
    for each_json in range(len(d)):
        for each_title in range(len(head)):
            class_info[head[each_title]] = d[each_json][str(each_title)]
        info['Class ' + str(each_json)] = class_info
        class_info = {}
    return info

def scrape_course(major="ME", class_num="451", term="W18"):
    """A function to scrape the Oregon State University 'General Catalog & Schedule of Classes'. All of the relevant data
    is stored in tables on the webpage. The data is sifted through to find course information, and then a dictionary is created
    to hold the data, and it is passed to a Course object.
    This function returns the Course object with all of the relevant course data from the OSU webpage.
    """

    url = "http://catalog.oregonstate.edu/CourseDetail.aspx?subjectcode={}&coursenumber={}&term={}".format(major, class_num, to_url(term))    # define url
    
    # get table data from webpage
    data = get_data(url)   
    if data == False:
        return 'No classes offered during the specified time.'


    # assign data to variable           
    d = data[0]

    # assign class name to variable
    class_name = get_class_name(data[1])
    
    # make a list of the headers
    head = data[2]

    # dictionary to hold course data
    info = get_dict(d, head)
    
    
    return Course(info, class_name)
    
class Course:
    """A simple class that stores and returns values from the Oregon State University course catalog"""

    def __init__(self, data, class_name):
        self.data = data
        self.class_name = class_name

    def __str__(self):
        print(self.class_name + '\n')
        omit(self.data)
        return ''

if __name__ == "__main__":

    c = scrape_course('ME', '498', 'Sp18')
    print(c)
    