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
    # Need to find a better way to handle the wierd way that the date is changed on the website.
    # For example, Fall 2018 has the value 201901
    # Need to figure out when year is set ahead by one, and when behind
    year = int(ts[-2:])
    year = str(year)
    if ts[0] == 'S' or ts[0] == 's':
        if ts[1] == 'u' or ts[1] == 'U':    # summer term e.g. '201801'
            return '20' + year + '00'
        return '20' + year + '03'           # spring term e.g. '201803'
    if ts[0] == 'F' or ts[0] == 'f':
        return '20' + year + '01'           # fall term e.g. '201801'
    return '20' + year + '02'               # winter term e.g. '201802'


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
    
    
    return Course(major, class_num, term, info, class_name)
    
class Course:
    """A simple class that stores and returns values from the Oregon State University course catalog"""

    def __init__(self,major="ME", class_num="451", term="W18", data="", class_name=""):
        self.major = major
        self.class_num = class_num
        self.term = term
        self.data = data
        self.class_name = class_name

    # For all class methods, a try/except error handle needs to be implemented in the case that no data was scraped.
    # This could be due to the user putting in the wrong term, or seeking a term that the course catalog has no information for.
    
    def __str__(self):
        print(self.class_name + '\n')
        # print("There are " + str(len(self.data) - 1) + " available classes during " + self.term +  ": \n")
        omit(self.data)
        return ''

    # def get_data(self):
    #     return self.data['Class 0']['Type']

    # def get_dow(self, class_num="Class 1"):
    #     times = self.data["Class 1"]["Day/Time/Date"]
    #     print(self.data[class_num]["Day/Time/Date"][:3])
    #         #print(self.data["Class " + str(i)]["Term"])

    # def get_tod(self, class_num="Class 1"):
    #     print(self.data[class_num]["Day/Time/Date"][3:12])

    
        

if __name__ == "__main__":

    c = scrape_course('ME', '451', 'W19')
    print(c)
    #print(c.get_clean_info())
    #c.get_classes()