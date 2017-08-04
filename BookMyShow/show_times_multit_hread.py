'''
Created on 19-Jun-2017

@author: M Manoj
@contact: mmanoj@apikdd.com
'''
import time
import threading
from Database import DataBase
from show_times import BmsShowTimes
class BMS_Times:
    def __init__(self):
        self.domain_ip = ''
        self.website_thumbnail = ''
    def bms_showtime_count(self,thread_name,starts,stops):
        connection=DataBase().connection()
        cursor=connection.cursor()
        BmsShowTimes().getBmsShowTimes(starts, stops)
    def run(self):
        connection=DataBase().connection()
        cursor=connection.cursor()
        cursor.execute("truncate collections.bms_showtimes")
        connection.commit()
        print DataBase().showtimesCountQuery
        cursor.execute(DataBase().showtimesCountQuery)
        count=cursor.fetchall()
        count=count[0][0]
        limit=1
        start=1
        stop=2000
        loopCount=2000
        try:
            limit=count/loopCount
        except:
            limit=15
            pass
        for i in range(0,limit+1):
            t = threading.Thread(target=self.bms_showtime_count,args=("thread_name_"+str(i),start,stop))
            t.start()
            start=stop+1
            stop=start+loopCount-1
        try:
            connection.close()
            print "Initial Connection Closed"
        except:
            print "Initial connection Not closed"
if __name__ == '__main__':
    d = BMS_Times()
    d.run()