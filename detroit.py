__author__ = 'dainaandries'
# -*- coding: utf-8 -*-

import pickle
import csv

# deserialize pickles from previous three scripts:
# detroit_data_pickled.py, detroit_dates_pickled.py,
# detroit_keythemes_pickled.py
input = open('detroit_pickle', 'rb')
input_dates = open('detroit_date_pickle', 'rb')
input_keywords = open('detroit_keywords_pickle', 'rb')

header = pickle.load(input)
clean_dataset = pickle.load(input)
abstract_col = pickle.load(input)

dates = pickle.load(input_dates)
rev_dates = pickle.load(input_dates)

keywords = pickle.load(input_keywords)

input.close()
input_dates.close()
input_keywords.close()

# manipulate before writing to csv
# manipulate keywords
formatted_keywords = []
for i in keywords:
    i = i.replace(', ', '###')
    formatted_keywords.append(i)

# manipulate form of dates
dates_dictionary = {'Jan':'01', 'Feb':'02', 'Mar': '03', 'Apr':'04', 'May':'05',
                    'Jun': '06', 'Jul': '07', 'Aug':'08', 'Sep':'09', 'Oct':'10',
                    'Nov':'11', 'Dec':'12'}

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

formatted_rev_dates = []
for i in rev_dates:
    i = i.split(' ')
    month = i[0]
    if i[0] != '':
        i[0] = dates_dictionary[month]
        i = i[2] + '-' + i[0] + '-' + i[1]
        i = i.rstrip(',')
        formatted_rev_dates.append(i)
    else:
        formatted_rev_dates.append(i[0])

# merge data
for a, b in zip(abstract_col, clean_dataset):
    b[3] = a

for a, b in zip(formatted_dates, clean_dataset):
    b[12] = str(a).encode('utf8')

for a, b in zip(formatted_rev_dates, clean_dataset):
    b[13] = str(a).encode('utf8')

for a, b in zip(formatted_keywords, clean_dataset):
    b[4] = a

# format titles
for i in clean_dataset:
    date = i[12].split('-')
    year = date[0]
    i[2] = i[2].replace('_', ' ') + ': ' + 'Detroit, Michigan' + ', ' + year

# write to csv
output = open('detroit_metadata.csv', 'w')
writer = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

writer.writerow(header)
for datum in clean_dataset:
   writer.writerow(datum)

output.close()












