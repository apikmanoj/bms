'''
Created on 16-Jun-2017

@author: H-7
'''
from bs4 import BeautifulSoup
import re
import requests
import string
import json
import mysql.connector
from Database import DataBase
from mysql.connector import MySQLConnection, Error
connection=DataBase().connection()
cursor = connection.cursor()
query='SELECT distinct(city) FROM moviesfyi_stage.bk_theaters where theater_url is null;'
cursor.execute(query)
results = cursor.fetchall()
city=""
k=1
for j in results:
    if(" " in j[0]):
        city=j[0].replace(" ","-")
        print city
        print "++++++++++++"
        if("(" in city):
            city=city.replace("(", "")
            city=city.replace(")", "")
        else:
            city=j[0].replace(" ","-")
    else:
        city=j[0]
    print city
    url="https://in.bookmyshow.com/"+city+"/cinemas"
    r=requests.get(url)
    data = r.text
    soup = BeautifulSoup(data,"lxml")
    #print soup
    for list in soup.find_all('div' , class_="__cinema-text"):
        #print list
        list=str(list)
        texte=list[:list.rindex('"')]
        #print texte
        turl=texte[texte.rindex('"')+1:]
        print turl
        theatrecode=turl[turl.rindex("/")+1:]
        print theatrecode
        print"-------------"
        update_query="update moviesfyi_stage.bk_theaters set theater_url='"+turl+"' "+"where theater_code='"+theatrecode+"';"
        cursor.execute(update_query)
        connection.commit()