import threading
from multiprocessing import Queue
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import datetime
import imaplib
import email
import random
import HTMLParser

startID = {
    "2314": 647760737,
    "2334": 647761073,
    "2308": 647760593,
    "2310": 647760641,
    "2312": 647760684,
    "2316": 647760785,
    "2318": 647760833,
    "2326": 647760881,
    "2328": 647760929,
    "2330": 647760977,
    "2332": 647761025,
    "2336": 647761121,
    "2338": 647761169,
    "2501": 647761217,
    "2528": 647761313,
    "2574": 648692976,
}

username = ['colinmai','bliu00','andypan','nlama','alexcha','phugnguyen','francispyon']
password = ['Missamerica1!','Roofsniper1','61109393Ap$$','Nitrodum!12','#Pickle1998','Pk2liv3pn!','Thelong1']
lenGMAIL = len(username)

class parseLinks(HTMLParser.HTMLParser):
    def handle_starttag(self, tag, attrs):
        global global_futures_fair_value
        if tag == 'a':
            for name, value in attrs:
                if name == 'href':
                    linkList.append(str(value))

def sleep():
    time.sleep(random.randint(1,2))

def gmailLogin(username, password):
    username = username + '@ucsb.edu'
    M = imaplib.IMAP4_SSL('imap.gmail.com')
    M.login(username, password)
    M.select('Inbox')
    rv, data = M.search(None, 'ALL')
    mail_ids = data[0]
    id_list = mail_ids.split()
    latest_email_id = int(id_list[-1])
    typ, msg_data = M.fetch(latest_email_id, '(RFC822)')
    msg = email.message_from_string(msg_data[0][1])
    msg = str(msg.get_payload()[1])
    linkParser = parseLinks()
    linkParser.feed(msg)
    M.close()
    M.logout()
    browser = webdriver.Chrome()
    browser.get(linkList[0])
    sleep()
    browser.find_element_by_id('rm_confirm_link').click()
    browser.close()

def roomReserve(username, password, ID):
    browser = webdriver.Chrome()
    browser.get('https://libcal.library.ucsb.edu/rooms.php?i=12405')
    select = Select(browser.find_element_by_class_name('ui-datepicker-month'))
    select.select_by_value(str(date.month - 1))
    time.sleep(.25)
    browser.find_element_by_link_text(date.strftime('%d').lstrip('0')).click()
    time.sleep(1)
    #click 4 time slots, total 2 hours
    for x in range(4):
        ID = str(ID)
        browser.find_element_by_id(ID).click()
        ID = int(ID)
        ID += 1
        time.sleep(.25)

    #get to the next screen
    browser.find_element_by_name('Continue').click()
    browser.find_element_by_id('s-lc-rm-sub').click()

    #loginUCSB
    browser.find_element_by_id('username').send_keys(username)
    browser.find_element_by_id('password').send_keys(password)
    sleep()
    browser.find_element_by_name('submit').click()

    #send Group Name
    browser.find_element_by_name('nick').send_keys('FBI INTERVIEWS')
    browser.find_element_by_name('Submit').click()
    print datetime.datetime.now()
    sleep()
    browser.close()
    browser.quit()

def main(targetTime, targetRoom):
    startDate = datetime.datetime(2018, 11, 1, 0, 0)
    idate = datetime.datetime.now()
    timeSchedule = targetTime
    roomNumber = targetRoom
    id = str(roomNumber)

    tdate = datetime.datetime(idate.year, idate.month, idate.day, timeSchedule, 0)
    date = tdate + datetime.timedelta(days = 14)
    global date

    diffDay = date - startDate
    twelveAM = startID[id] + 816*diffDay.days
    idList = []
    idList.append(twelveAM)
    newID = startID[id] + 816*diffDay.days + 2*(diffDay.seconds/3600)

    for x in range(lenGMAIL-1):
        idList.append(newID)
        newID += 4
    idList = list(reversed(idList))
    # print idList

    thread_list = []
    start = time.time()
    for i in range (lenGMAIL):
        thread = threading.Thread(target = roomReserve, args = (username[i],password[i],idList[i],))
        thread_list.append(thread)
        thread.start()

    for thread in thread_list:
        thread.join()

    print 'total time taken:', time.time()-start

    for k in range(lenGMAIL):
        linkList = []
        global linkList
        try:
            gmailLogin(username[k], password[k])
            print 'Successful confirmation for:', username[k]
        except Exception:
            print 'an error has occured with the following username, trying next username', username[k]
            pass
# while True:
# wait for midnight
while datetime.datetime.now().hour != 0:
    print 'sleeping ... ' , datetime.datetime.now()
    time.sleep(1)
main(12, 2314)
# print 'sleeping for one hour...'
# time.sleep(3600)
