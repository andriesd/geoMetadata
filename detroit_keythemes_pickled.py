__author__ = 'dainaandries'

# NOTE: third script run to get data from Detroit Open Data Website

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
# scrape key words
# store in ordered list named 'keywords'
# add blanks to maintain order
driver = webdriver.PhantomJS()

count = 0
keywords = []
for link in meta_links:
    if link == '':
        count += 1
        keywords.append(link)
        print str(count) + ' ' + '...'

    else:
        count += 1
        driver.get(link)
        # try and except to account for variations in web page development
        # in case xpath needs to point to div[5]
        try:
            b = driver.find_element_by_xpath('//*[@id="aboutSection"]/div[@class="innerContainer"]/'
                                          'div[@class="fullHeight"]/div[@class="aboutDataset"]/'
                                          'div[5]/dl/dd[3]/span')
            keyword_group = b.get_attribute('innerHTML')
            keywords.append(keyword_group)
            print str(count) + ' ' + keyword_group

        except:
            # in case xpath needs to point to div[4]
            try:
                b = driver.find_element_by_xpath('//*[@id="aboutSection"]/div[@class="innerContainer"]/'
                                          'div[@class="fullHeight"]/div[@class="aboutDataset"]/'
                                          'div[4]/dl/dd[3]/span')
                keyword_group = b.get_attribute('innerHTML')
                keywords.append(keyword_group)
                print str(count) + ' ' + keyword_group

            except:
                print str(count) + ' ' + 'failed'


driver.close()

# pickle (serialize) the publication and revision dates
# to be opened (deserialized) in detroit.py
output = open("detroit_keywords_pickle", 'wb')
pickle.dump(keywords, output)

output.close()