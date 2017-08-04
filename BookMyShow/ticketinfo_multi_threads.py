'''
Created on 19-Jun-2017

@author: M Manoj
@contact: mmanoj@apikdd.com
'''
import threading
from Database import DataBase
from ticket_info import BmsAvailableSeats
class BMS_Seats:
    def __init__(self):
        self.domain_ip = ''
        self.website_thumbnail = ''
    def bms_ssid_count(self,thread_name,starts,stops):
        print thread_name
        print "start=="+str(starts)+" stop=="+str(stops)
        BmsAvailableSeats().ticketsinfo(starts, stops)     
    def run(self):
        connection=DataBase().connection()
        cursor=connection.cursor()
        cursor.execute(DataBase().trunk_ticket_info)
        connection.commit()
        cursor.execute(DataBase().ssidcountquery)
        count=cursor.fetchall()
        count=count[0][0]
        print "data==",count
        limit=1
        start=0
        stop=100
        loopCount=100
        try:
            limit=count/loopCount
        except:
            limit=15
            pass
        print "no of threads==",limit+1
        for i in range(0,limit+1):
            t = threading.Thread(target=self.bms_ssid_count,args=("thread_name_"+str(i),start,stop))
            t.start()
            start=start+100
            stop=100
        try:
            connection.close()
            print "Initial Connection Closed"
        except:
            print "Initial connection Not closed"
if __name__ == '__main__':
    d = BMS_Seats()
    d.run()