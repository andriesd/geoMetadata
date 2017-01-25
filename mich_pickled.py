__author__ = 'dainaandries'

# NOTE: first script run to get data from Michigan Open Data Website

import pickle
from selenium import webdriver

# import csv (data from GeoNetwork API in CSV format)
# clean data and create a list of lists (equivalent to a table)
clean_dataset = []
file_input = open('mich.csv', 'rU')
for line in file_input:
    # some cells contain commas
    # following code contains workaround to not split
    # csv data according to the wrong commas
    # extraneous quotes also stripped
    line = line.strip().rsplit(',', 13)
    first = line[0]
    divided = first.split(',', 2)
    abstract = divided[2]
    if abstract.startswith('"'):
        # print '--------------'
        abstract = abstract.split('",')
        abstract[0] = abstract[0].lstrip('"')
    else:
        abstract = abstract.split(',', 1)
    # print abstract

    clean_data = divided[0:2] + abstract + line[1:]
    # NOTE: code for special case
    if len(clean_data) == 18:
        del clean_data[5]
        clean_data[4] = clean_data[4]+'Michigan######Menominee County'
    # print len(clean_data)
    # print clean_data

    clean_dataset.append(clean_data)

header = clean_dataset[0]
del clean_dataset[0]

# NOTE: exploratory code
# for i in clean_dataset:
#     if i[8].startswith('http://gis.michigan.opendata.arcgis.com/datasets'):
#         print i[8]
#     else:
#         print 'other source'

# NOTE: discovered zip files are shapefiles for download
# NOTE: all zip files labeled as shapefiles
for i in clean_dataset:
    if i[7].endswith('.zip'):
        i[11] = 'Shapefile shapefile'

# webscraping with PhantomJS browser
# scrape publication dates
# store in ordered list named 'publication_dates'
# add blanks to maintain order
driver = webdriver.PhantomJS()
driver.set_window_size(7000, 7000)

count = 0
publication_dates = []
for i in clean_dataset:
    if i[8].startswith('http://gis.michigan.opendata.arcgis.com/datasets/'):
        try:
            print i[8]
            driver.get(i[8])
            b = driver.find_element_by_xpath('//*[@id="dataset-meta-list"]/li[2]/span[@class="info-wrapper"]/a').click()
            # print b.get_attribute('innerHTML')
            handles = driver.window_handles
            driver.switch_to.window(handles[-1])
            driver.implicitly_wait(5)
            b2 = driver.find_element_by_xpath('//*[@id="esri_Evented_0"]/section/aside/section/p[4]')
            count += 1
            date = b2.get_attribute('innerHTML')
            print count, date
            publication_dates.append(date)

        except:
            count += 1
            print count, 'no page exists or no data was retrieved'
            publication_dates.append('')

    else:
        # in the absence of the right kind of link:
        count += 1
        print count,  ''
        publication_dates.append('')

driver.close()

# pickle (serialize) dates
# to be opened (deserialized) in mich.py
output = open("michigan_dates_pickle", 'wb')
pickle.dump(header, output)
pickle.dump(clean_dataset, output)
pickle.dump(publication_dates, output)

output.close()


# NOTE: old version of code for scraping (clicking different links):
  # try:
        #     # has visible link 'More Metadata'
        #
        #     driver.get(i[8])
        #     b2 = driver.find_element_by_xpath('//*[@id="dataset-attributes-region"]/div[@class="attributes-view"]/div[1]/'
        #                                       'span[@id="dataset-description"]/div[@class="description-inner"]/div[2]/a').click()
        #     handles = driver.window_handles
        #     print handles
        #     driver.switch_to.window(handles[-1])
        #     b3 = driver.find_element_by_xpath('/html/body/dl[1]/dd/dl/dd[1]/dl/dd/dl/dt[2]')
        #     b3two = driver.find_element_by_xpath('/html/body/dl[1]/dd/dl/dd[1]/dl/dd/dl/dt')
        #     count += 1
        #     print count, 'button present', b3.get_attribute('innerHTML'), b3two.get_attribute('innerHTML')
        #
        #
        # except:
        #     try:
        #         # dropdown
        #
        #         driver.get(i[8])
        #         b = driver.find_element_by_xpath('//*[@id="dataset-attributes-region"]/div[@class="attributes-view"]'
        #                                          '/div[1]/div[@id="view-full-description"]/i').click()
        #         handles = driver.window_handles
        #         driver.switch_to.window(handles[-1])
        #         b2 = driver.find_element_by_xpath('//*[@id="dataset-attributes-region"]/div[@class="attributes-view"]/div[1]/'
        #                                               'span[@id="dataset-description"]/div[@class="description-inner"]/div[2]/a').click()
        #         handles = driver.window_handles
        #         driver.switch_to.window(handles[-1])
        #         b3 = driver.find_element_by_xpath('/html/body/dl[1]/dd/dl/dd[1]/dl/dd/dl/dt[2]')
        #         count += 1
        #         print count, 'dropdown', b3.get_attribute('innerHTML')
        #
        #
        #     except:
        #         count += 1
        #         print count, 'failed'
