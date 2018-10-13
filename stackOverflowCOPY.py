import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import collections
import datetime
import smtplib
import imaplib
import email
import random
import quopri
import HTMLParser
import time


startDate = datetime.datetime(2018, 10, 18 , 0, 0)
userInfo = {'USERNAME':'PASSWORD'}

startID = {
    "2314": 647749313,
    "2334": 647749649,
    "2308": 647749169,
    "2310": 647749217,
    "2312": 647749265,
    "2314": 647749313,
    "2316": 647749361,
    "2318": 647749409,
    "2326": 647749457,
    "2328": 647749505,
    "2330": 647749553,
    "2332": 647749601,
    "2334": 647749649,
    "2336": 647749697,
    "2338": 647749745,
    "2501": 647749793,
    "2528": 647749889,
    "2574": 648692304,
}


id = str(2314) # room number here
tDate = datetime.datetime(2018, 10, 4, 13, 0)
date = tDate + datetime.timedelta(days = 15) # desired date/time here
print "Desired date and time", date
diffDay = int(date.strftime('%d')) - int(startDate.strftime('%d'))
print "diffday", diffDay
diffHour = int(date.strftime('%H')) - int(startDate.strftime('%H'))
print "diffhour", diffHour

newID = startID[id] + 816*diffDay + diffHour*2
print "newID", newID

class parseLinks(HTMLParser.HTMLParser):
    def handle_starttag(self, tag, attrs):
        global global_futures_fair_value
        if tag == 'a':
            for name, value in attrs:
                if name == 'href':
                    #print name
                    # print str(value)
                    linkList.append(str(value))


def gmailLogin(userName, password):
    #TODO: implement try and catch for emails that didnt get the confirmation link
    #catch: record and print email where it failed, move onto next email/password pair

    userName = userName + '@ucsb.edu'
    M = imaplib.IMAP4_SSL('imap.gmail.com')
    M.login(userName, password)
    M.select('Inbox')

    rv, data = M.search(None, 'ALL')
    mail_ids = data[0]
    id_list = mail_ids.split()
    latest_email_id = int(id_list[-1])
    #implement method for finding email id with subject 'Please confirm your booking!'
    typ, msg_data = M.fetch(latest_email_id, '(RFC822)')
    msg = email.message_from_string(msg_data[0][1])
    msg = str(msg.get_payload()[1])
    #msg = quopri.decodestring(msg)

    linkParser = parseLinks()
    linkParser.feed(msg)
    M.close()
    M.logout()
    print linkList[0]
    #return str(linkList[0])
    browser = webdriver.Chrome()
    browser.get(linkList[0])
    #click link
    sleep()
    browser.find_element_by_id('rm_confirm_link').click()
    browser.close()



def sleep():
    time.sleep(random.randint(1,2))

def roomReserve(userName, password, newID):
    browser = webdriver.Chrome()
    browser.get('https://libcal.library.ucsb.edu/rooms.php?i=12405')
    sleep()
    browser.find_element_by_link_text(date.strftime('%d').lstrip("0")).click() # click date
    time.sleep(3)
    for x in range (0,4):
        sleep()
        print "NEW ID HERE", newID
        newID = str(newID)
        browser.find_element_by_id(newID).click()
        newID = int(newID)
        newID += 1


    sleep()
    browser.find_element_by_name('Continue').click()
    sleep()
    browser.find_element_by_id('s-lc-rm-sub').click()

    #loginUCSB
    sleep()
    browser.find_element_by_id('username').send_keys(userName)
    sleep()
    browser.find_element_by_id('password').send_keys(password) #password is placeholder here
    sleep()
    browser.find_element_by_name('submit').click()

    #send Groupname: name="nick" id="nick"
    sleep()
    browser.find_element_by_name('nick').send_keys('2.0 Fri3nd Gr0up')
    sleep()
    browser.find_element_by_name('Submit').click()
    sleep()

    #confirmEmails after all the rooms have been reserved, error on their side
    #maybe it takes longer to send links to confirm all the rooms

    #signout?

    #close browser
    browser.close()
    # browser.quit()


#wait for midnight
while datetime.datetime.now().hour != 0:
    print 'Last checked', datetime.datetime.now().second
    time.sleep(1)

#reserve rooms for each username
for userName, password in userInfo.items():
    #TODO:not sure exactly why gamilLogin is not updating userName and password, maybe something
    #to do with try and except, let's figure it out tomorrow
    #only confirmed the first one, so im pretty sure the gamilLogin is not updating
    #try to see which rooms are available and reserve accordingly
    #problem with ucsb, sometimes after reserving, the email does not show up to confirm
    #linkList = []
    #TODO: optimize for room reserve time, rather than do it one at a time, do them one
    #after the other
    try:
        roomReserve(userName,userInfo[userName], newID)
        sleep()
        newID = newID + 4
        print "postID here", newID
    except Exception:
        print "an error has occured with the follow username, trying next username/password combination...", userName
        pass

#confirm emails for each username
for userName, password in userInfo.items():
    linkList = []
    try:
        sleep()
        gmailLogin(userName,userInfo[userName])
        print "Successful confirmation for:" ,userName
    except Exception:
        print "an error has occured with the follow username, trying next username/password combination...", userName
        pass
