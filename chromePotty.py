#need to import beautifulsoup
from bs4 import BeautifulSoup
#need to import datetime
import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import collections
import time

browser = webdriver.Chrome()

browser.get('https://my.sa.ucsb.edu/public/curriculum/coursesearch.aspx')
select = Select(browser.find_element_by_id('ctl00_pageContent_courseList'))
selectQuarter = Select(browser.find_element_by_id('ctl00_pageContent_quarterList'))
options = select.options

keyArray = []
for o in options:
    poop = o.text.split('-')
    del poop[0]
    poop[0] = poop[0].encode().lstrip()
    keyArray.append(poop[0])
#print keyArray, list of options from the dropdown menu

for key in keyArray:
    browser.get('https://my.sa.ucsb.edu/public/curriculum/coursesearch.aspx')
    select = Select(browser.find_element_by_id('ctl00_pageContent_courseList'))
    select.select_by_value(key)
    #selectQuarter.select_by_value(quarterValue)
    browser.find_element_by_name('ctl00$pageContent$searchButton').click()

    html = browser.page_source
    soup = BeautifulSoup(html, 'lxml')

    CourseInfoRow = soup.findAll("tr", {"class":"CourseInfoRow"})
    for rows in CourseInfoRow:
        listID = []
        courseID = rows.get_text().encode('utf-8').strip().split('\n')[0]
        listID.append(courseID)
        for td in rows:
            try:
                lotion = td.get_text().encode().split('\n')
                i = 0
                for spaces in lotion:
                    lotion[i] = spaces.strip()
                    i += 1
                lotion = list(filter(None, lotion))
                listID.append(lotion)
            except Exception:
                pass
        del listID[9]
        del listID[1]
        for x in range(1, len(listID)):
            length = len(listID[x])
            if length == 0:
                listID[x] = ''
            elif length == 1:
                listID[x] = listID[x][0]
        print listID
    #TODO: split up times to ['starttime','endtime']
    #TODO: split up days to ['M','W','F']
    # time.sleep(2)
browser.close()
browser.quit()
