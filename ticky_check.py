#!/usr/bin/env python3

import re
import operator
import csv

#save the log as a variable
with open ("syslog.log") as f:
    text = f.readlines()

#counts the amount of times each error appears
e = {}

for line in text:
    t = re.search(r"ERROR (.*) \(", line)
    if t:
        if t.group(1) not in e:
            e[t.group(1)] = 1
        else:
            e[t.group(1)] += 1

#sorts the errors by number of occurencies
errors = sorted(e.items(), key = operator.itemgetter(1), reverse=True)

#save errors and occurencies to a csv file
with open('error_message.csv','w') as out:
    csv_out=csv.writer(out)
    csv_out.writerow(["Error", "Count"])
    for row in errors:
        csv_out.writerow(row)

#counts the usage for each user
users = {}
for line in text:
    a = re.search(r"ticky: (.*?) .*\((.*)\)", line)
    if a:
        if a.group(2) not in users and a.group(1) == "ERROR":
            users[a.group(2)] = [0,1]
        elif a.group(2) not in users and a.group(1) == "INFO":
            users[a.group(2)] = [1,0]
        elif a.group(1) == "ERROR":
            users[a.group(2)][1] =  users[a.group(2)][1] + 1
        elif a.group(1) == "INFO":
            users[a.group(2)][0] =  users[a.group(2)][0] + 1

sorted_users = sorted(users.items())

per_user = []

for i in sorted_users:
    per_user.append((i[0], i[1][0], i[1][1]))

with open('user_statistics.csv','w') as out2:
    csv_out=csv.writer(out2)
    csv_out.writerow(["Username", "INFO", "ERROR"])
    for row in per_user:
        csv_out.writerow(row)