from bs4 import BeautifulSoup
from email.mime.text import MIMEText
#from email.message import EmailMessage
import requests
import smtplib
import datetime
import MySQLdb as mdb
import MySQLdb.cursors

conn = mdb.connect('localhost', 'root', 'maryamsaqib2000', 'myflaskapp', cursorclass=MySQLdb.cursors.DictCursor) 


def getEmail(userId):
    cur = conn.cursor()
    cur.execute("select * from users where id = '%s'" % userId)
    result = cur.fetchone()
    if result:
        email = result['email']
        return email
    else:
        print('no result')
    return 'no result'

def getUrl(productid):
    #287281872 not on offer
    #250106683 on offer
    id = productid #Make this dynamic
    return 'https://www.tesco.com/groceries/en-GB/products/' + str(id)

def sendEmail(emailaddress, productname):
    debuglevel = 0
    smtp = smtplib.SMTP()
    smtp.set_debuglevel(debuglevel)
    smtp.connect('smtp.gmail.com', 25)
    smtp.starttls()
    smtp.login('supermarketoffercontrolservice@gmail.com', 'Password22')
    from_addr = 'supermarketoffercontrolservice@gmail.com'
    to_addr = emailaddress
    subj = 'supermarketoffercontrol - {} is on offer'.format(productname)
    date = datetime.datetime.now().strftime( '%d/%m/%Y %H:%M' )
    message_text = 'Hello\nThis is a mail from your server to let you know that ' + productname + ' is on offer at Tesco\n\nThank you\n'
    msg = 'From: %s\nTo: %s\nSubject: %s\nDate: %s\n\n%s' % ( from_addr, to_addr, subj, date, message_text )
    smtp.sendmail(from_addr, to_addr, msg)
    smtp.quit()

cur = conn.cursor() 
cur.execute("select * from subscriptions")
rows = cur.fetchall() 
for row in rows:
    #res = requests.get('https://www.tesco.com/groceries/en-GB/products/254888441')
    #print row
    res = requests.get(getUrl(row['productid']))
    soup = BeautifulSoup(res.text, 'lxml')
    #is product on offer
    if soup.findAll("div", {"class": "icon-offer-flash-group"}):
        #product is on offer
        #print('product {} is on offer'.format(row['productname']))
        sendEmail(getEmail(row['userid']), row['productname']) 
        #print 'test' 
    else:
        print('product is not on offer')