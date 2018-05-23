#!/usr/bin/env python3

def omit(data):
    total = 0
    for i in data:
        if i == "Class 0":
            pass
        elif data[i]["Type"] == "Laboratory":
            pass
        else:
            print(i + ": " + data[i]["Type"] + "\t " + data[i]["Instructor"] + "\t " + data[i]["Day/Time/Date"][:3] + "\t " + data[i]["Day/Time/Date"][3:12])  
            total += 1
    return total