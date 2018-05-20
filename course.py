#!/usr/bin/env python
# Sources:
# 1. https://www.crummy.com/software/BeautifulSoup/bs4/doc/


from bs4 import BeautifulSoup
import urllib
import pandas as pd
import requests
import json


url = "http://catalog.oregonstate.edu/CourseDetail.aspx?Columns=afghijklmnopqrstuvwyz{&SubjectCode=ME&CourseNumber=451&Term=202000"

def to_url(ts):
    # Need to find a better way to handle the wierd way that the date is changed on the website.
    # For example, Fall 2018 has the value 201901
    # Need to figure out when year is set ahead by one, and when behind
    year = int(ts[-2:])+1
    year = str(year)
    if ts[0] == 'S' or ts[0] == 's':
        if ts[1] == 'u' or ts[1] == 'U':    # summer term e.g. '201801'
            return '20' + year + '00'
        return '20' + year + '03'           # spring term e.g. '201803'
    if ts[0] == 'F' or ts[0] == 'f':
        return '20' + year + '01'           # fall term e.g. '201801'
    return '20' + year + '02'               # winter term e.g. '201802'
        
    return year

def scrape_course(major="ME", class_num="451", term="W18"):
    """A function to scrape the Oregon State University 'General Catalog & Schedule of Classes'. All of the relevant data
    is stored in tables on the webpage. The data is sifted through to find course information, and then a dictionary is created
    to hold the data, and it is passed to a Course object.
    This function returns the Course object with all of the relevant course data from the OSU webpage.
    """

    # get a json object with all of the relevant course information from the HTML table on the webpage
    url = "http://catalog.oregonstate.edu/CourseDetail.aspx?subjectcode={}&coursenumber={}&term={}".format(major, class_num, to_url(term))    # define url
    f = urllib.request.urlopen(url)             # Fetch DOM at url
    soup = BeautifulSoup(f, "lxml")
    table = soup.find_all('table')[4]           # Table with class information
    df = pd.read_html(str(table))
    raw_list = df[0].to_json(orient='records')  # get data in JSON format
    d = json.loads(raw_list)                    # convert raw_list to JSON object
    print(d)
    # make a list for the class description
    class_title = soup.h3.contents[2].strip().split('\n')
    title = [i.strip() for i in class_title]                # e.g. ['ME 311', 'INTRODUCTION TO THERMAL-FLUID SCIENCES', '(4).']
    class_name = str(title[0] + ': ' + title[1]).replace('.', '')
    
    # make a list of the headers
    head = [d[0][(str(i))] for i in range(len(d[0]))]

    # create a dictionary with correct key, value pairs
    # dictionary should contain sub-dictionaries with class listings
    # info is a dictionary that contains all of the class information
    # each class offered on the webpage contains its own dictionary with appropriate keys and values, regarding course information
    info = {}
    class_info = {}     # place holder
    for each_json in range(len(d)):
        for each_title in range(len(head)):
            class_info[head[each_title]] = d[each_json][str(each_title)]
        info['Class ' + str(each_json)] = class_info

    print(info)
    print('##########################################################')
    return Course(major, class_num, term, info, soup, class_name)
    
class Course:
    """A simple class that stores and returns values from the Oregon State University course catalog"""

    def __init__(self,major="ME", class_num="451", term="W18", data="", soup="Beautiful Soup 4", class_name=""):
        self.major = major
        self.class_num = class_num
        self.term = term
        self.data = data
        self.soup = soup
        self.class_name = class_name

    def __str__(self):
        return self.class_name

    def get_data(self):
        return self.data['Class 0']['Type']

    def get_clean_info(self):
        print('\n')
        print('Instructor' + '\t' + 'Date/Time' + 3*'\t' + 'Lec/Lab' + 2*'\t' + 'Section')
        print('\n')
        for i in range(0, len(self.data)):
            print(self.data['Class ' + str(i)]['Instructor'] +'\t' + self.data['Class ' + str(i)]['Day/Time/Date'] + '\t' + self.data['Class ' + str(i)]['Type'] + '\t' + self.data['Class ' + str(i)]['Sec'])
        return '\n'

if __name__ == "__main__":
    c = scrape_course('ME', '451', 'F18')
    print(c)
    #print(c.get_clean_info())