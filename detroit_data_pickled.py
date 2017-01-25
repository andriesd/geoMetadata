__author__ = 'dainaandries'
# -*- coding: utf-8 -*-

# NOTE: first script run to get data from Detroit Open Data Website

from selenium import webdriver
import pickle

# import csv (data from GeoNetwork API in CSV format)
# clean data and create a list of lists (equivalent to a table)
clean_dataset = []
file_input = open('detroit.csv', 'rU')
for line in file_input:
    line = line.strip().rsplit(',', 11)
    first = line[0]
    #print first
    first = first.split(',', 5)
    #print first
    first[5] = first[5].strip(',').strip('"')
    clean_data = first + line[1:]
    clean_dataset.append(clean_data)

# set aside header in header variable
header = clean_dataset[0]
del clean_dataset[0]

# index for retrieval, but not for final printout
# for final printout 'clean_dataset' is better
# index = []
# for data in clean_dataset:
#     dct = dict(zip(header, data))
#     index.append(dct)

# print len(clean_dataset)
# print header.index('NEW_link_information')
# print header.index('NEW_link_download')

# NOT all rows had link_download information
# take 'sample' from row that does
# break down sample into constituent parts: API link and
# method and format of download
sample = clean_dataset[65]
url_split = sample[7].rsplit('?')
method_format = url_split[1]
resource = url_split[0][:-9]


# perform this transformation on other rows that don't have download_links
# concatenate 'resource', resource ID, and 'method_format'
for i in clean_dataset:
    url_facets = i[8].split('/')
    if len(url_facets) == 1:
        continue
    else:
        i[7] = resource + url_facets[5] + '?' + method_format

# store landing page links in ordered list
# add blanks to maintain order
# expand links to point to static 'about' page
meta_links = []
for i in clean_dataset:
    test_url = i[8]
    if test_url == '':
        meta_links.append(test_url)
    else:
        meta_links.append(test_url+'/about')

# webscraping with PhantomJS browser
# scrape abstracts
# store in ordered list named 'abstract_col'
# add blanks to maintain order
driver = webdriver.PhantomJS()

count = 0
abstract_col = []
for link in meta_links:
    # what to do if no link is there
    if link == '':
        count += 1
        abstract_col.append(link)
        print str(count) + ' ' + '...'

    else:
        count += 1
        driver.get(link)
        b = driver.find_element_by_xpath('//*[@id="aboutSection"]/div[@class="innerContainer"]'
                                         '/div[@class="fullHeight"]/div[@class="aboutDataset"]/'
                                         'div[@class="formSection"]/div[@class="sectionContent"]')
        b_children = b.find_elements_by_xpath('.//*')
        abstracts=[]
        for b_child in b_children:
            abstract = b_child.get_attribute('innerHTML')
            if abstract == '':
                continue
            else:
                abstract = abstract.encode('utf8')
                abstracts.append(abstract)
        abstract_col.append(' '.join(abstracts))
        print str(count) + ' ' + ' '.join(abstracts)

driver.close()

# pickle (serialize) the header, data, and abstracts
# to be opened (deserialized) in other scripts and detroit.py
output = open("detroit_pickle", 'wb')

pickle.dump(header, output)
pickle.dump(clean_dataset, output)
pickle.dump(abstract_col, output)

output.close()