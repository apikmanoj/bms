'''
Created on 19-Jun-2017

@author: M Manoj
@contact: mmanoj@apikdd.com
'''
from bs4 import BeautifulSoup
import requests
from Database import DataBase
import datetime

class BmsShowTimes:
    def getBmsShowTimes(self,starts,stops):
        connection=DataBase().connection()
        cursor = connection.cursor()
        sql="SELECT id,theater_url from collections.bms_theaters where theater_url is not null and id between "+str(starts)+" and "+str(stops)
        cursor.execute(sql)
        results = cursor.fetchall()
        date=datetime.date.today()
        date=str(date)
        date=date.replace("-", "")
        movies_ins=""
        count=0
        for j in results:
            testurl=j[1]
            url=j[1]
            da="https://in.bookmyshow.com"
            url=da+url
            r=requests.get(url)
            data = r.text
            soup = BeautifulSoup(data)
            query=""
            list=""
            for list in soup.find_all('a', href="javascript:;"):
                try:
                    list= list['onclick']
                    if ("blnVistaCine" in list):
                        list=list
                        list=list.split("callSeatLayout(")
                        teatinfo= list[1].split(")")
                        teatinfo=teatinfo[0].split(",")
                        theater_code= teatinfo[0]
                        sessionid=teatinfo[1]
                        movie_code=teatinfo[2]
                        showtime=teatinfo[3]
                        date=date
                        query=query+"("+movie_code+",'',"+theater_code+",'',"+"'y','"+date+"',"+showtime+","+"'y',"+sessionid+"),"
                except:
                    ""
            query=query[:-1]
            insquery=DataBase().show_time_ssid +query
            try:
                    cursor.execute(insquery)
                    connection.commit()
            except:
                ""
        connection.close()