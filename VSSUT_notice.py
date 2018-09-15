from bs4 import BeautifulSoup
import re
import requests
from fake_useragent import UserAgent
import pymysql.cursors
from urllib.request import urlopen
from datetime import datetime

#connection
connection = pymysql.connect(host='localhost',user='root',password='',db='mysql')
url = 'http://www.vssut.ac.in/'                    # input your url here
file_name = 'notices.txt'              # output file name
cur =connection.cursor()
cur.execute("USE notice")
user_agent = UserAgent()

page = requests.get(url,headers={'user-agent':user_agent.chrome})
with open(file_name,'w') as file:
    file.write(page.content.decode('utf-8')) if type(page.content) == bytes else file.write(page.content)


def read_file():
    file = open('notices.txt')
    data = file.read()
    file.close()
    return data

soup = BeautifulSoup(read_file(),features="xml")
tableclass=soup.find_all(class_="table")
tags=tableclass[0].find_all("td",{"width":{70}})
link=tableclass[0].find_all(class_="readmore")


for a in link:
    atag=a.get_text()
    print(atag)
    cur.execute("INSERT INTO notices (`notice`) VALUES (%s)",(atag))
    cur.connection.commit()

for tag in tags:
    tdtag=tag.get_text()
    print(tdtag)
    datetime_object = datetime.strptime(tdtag,'%d-%m-%Y')
    s = datetime_object.strftime("%Y-%m-%d")
    cur.execute("INSERT INTO noticedata (`dt`) VALUES (%s)",(tdtag))
    cur.connection.commit()

cur.close()
connection.close()
   


