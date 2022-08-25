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
        user = a.group(2)
        msg_class = a.group(1)
        if user not in users:
            users[user] = {}
            users[user][msg_class] = 1
        
        elif msg_class not in users[user]:
            users[user][msg_class] = 1
        else:
            users[user][msg_class] += 1

#save users and statistics to a csv file
with open('user_statistics.csv','w') as out2:
    csv_out=csv.writer(out2)
    csv_out.writerow(["Username", "INFO", "ERROR"])
    for row in users:
        csv_out.writerow([row, users[row].get('INFO',0), users[row].get('ERROR',0)])
