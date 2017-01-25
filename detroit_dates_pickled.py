__author__ = 'dainaandries'

# NOTE: second script run to get data from Detroit Open Data Website

from selenium import webdriver
import pickle

# open pickle from detroit_data_pickled.py
# get clean_dataset
input = open('detroit_pickle', 'rb')

header = pickle.load(input)
clean_dataset = pickle.load(input)

input.close()

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
# scrape publication dates first, then revision dates
# store in two separate ordered lists:
# 'dates' and 'rev_dates'
# add blanks to maintain order
driver = webdriver.PhantomJS()

count = 0
dates = []
for link in meta_links:
    if link == '':
        count += 1
        dates.append(link)
        print str(count) + ' ' + '...'

    else:
        count += 1
        driver.get(link)
        b = driver.find_element_by_xpath('//*[@id="aboutSection"]/div[@class="innerContainer"]/'
                                         'div[@class="fullHeight"]/div[@class="aboutDataset"]/'
                                         'div[@class="aboutHeader clearfix"]/p[1]/span[@class="aboutCreateDate"]/'
                                         'span[@class="dateReplace"]')

        pub_date = b.get_attribute('innerHTML')
        dates.append(pub_date)
        print str(count) + ' ' + pub_date

count = 0
rev_dates = []
for link in meta_links:
    if link == '':
        count += 1
        rev_dates.append(link)
        print str(count) + ' ' + '...'

    else:
        count += 1
        driver.get(link)
        b = driver.find_element_by_xpath('//*[@id="aboutSection"]/div[@class="innerContainer"]/'
                                         'div[@class="fullHeight"]/div[@class="aboutDataset"]/'
                                         'div[@class="aboutHeader clearfix"]/p[2]/span[@class="aboutUpdateDate"]/'
                                         'span[@class="dateReplace"]')

        rev_date = b.get_attribute('innerHTML')
        rev_dates.append(rev_date)
        print str(count) + ' ' + rev_date

driver.close()

# pickle (serialize) the publication and revision dates
# to be opened (deserialized) in detroit.py
output = open("detroit_date_pickle", 'wb')
pickle.dump(dates, output)
pickle.dump(rev_dates, output)

output.close()