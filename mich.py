__author__ = 'dainaandries'
# -*- coding: utf-8 -*-

import pickle
import csv

# deserialize pickle from mich_pickled.py
input = open('michigan_dates_pickle', 'rb')

header = pickle.load(input)
clean_dataset = pickle.load(input)
pub_dates = pickle.load(input)

input.close()

# manipulate date formats
dates_dictionary = {'January':'01', 'February':'02', 'March': '03', 'April':'04', 'May':'05',
                    'June': '06', 'July': '07', 'August':'08', 'September':'09', 'October':'10',
                    'November':'11', 'December':'12'}

dates = []
for i in pub_dates:
    if len(i) > 0:
        i = i[9:]
        i = i.encode('utf8')
    dates.append(i)

formatted_dates = []
for i in dates:
    i = i.split(' ')
    month = i[0]
    if i[0] != '':
        i[0] = dates_dictionary[month]
        i = i[2] + '-' + i[0] + '-' + i[1]
        i = i.rstrip(',')
        # i = "="+'"'+i+'"'
        formatted_dates.append(i)
    else:
        formatted_dates.append(i[0])

# merge data
for a, b in zip(formatted_dates, clean_dataset):
    b[12] = str(a).encode('utf8')

# format titles
for i in clean_dataset:
    date = i[12].split('-')
    year = date[0]
    i[2] = i[2].replace('_', ' ') + ': ' + 'Michigan' + ', ' + year

# write to csv
output = open('mich_metadata.csv', 'w')
writer = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

writer.writerow(header)
for datum in clean_dataset:
   writer.writerow(datum)

output.close()