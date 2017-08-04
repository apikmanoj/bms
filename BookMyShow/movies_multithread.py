'''
Created on 19-Jun-2017

@author: M Manoj
@contact: mmanoj@apikdd.com
'''
import threading
from Database import DataBase
from bms_movies import BMS_movies

class BMS_Movie:
    def __init__(self):
        self.domain_ip = ''
        self.website_thumbnail = ''
    def bms_movie_count(self,thread_name,starts,stops):
        print thread_name
        print "start=="+str(starts)+" stop=="+str(stops)
        BMS_movies().getmovie(starts, stops)
    def run(self):
        connection=DataBase().connection()
        cursor=connection.cursor()
        # cursor.execute("truncate moviesfyi_stage.bk_movies")
        connection.commit()
        cursor.execute(DataBase().showtimesCountQuery)
        count=cursor.fetchall()
        count=count[0][0]
        print "data==",count
        limit=1
        start=1
        stop=300
        loopCount=300
        try:
            limit=count/loopCount
        except:
            limit=15
            pass
        print "no of threads==",limit+1
        for i in range(0,limit+1):
            t = threading.Thread(target=self.bms_movie_count,args=("thread_name_"+str(i),start,stop))
            t.start()
            start=stop+1
            stop=start+loopCount-1
        try:
            connection.close()
            print "Initial Connection Closed"
        except:
            print "Initial connection Not closed"
if __name__ == '__main__':
    d = BMS_Movie()
    d.run()