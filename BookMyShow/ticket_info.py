'''
Created on 19-Jun-2017

@author: M Manoj
@contact: mmanoj@apikdd.com
'''
import requests
import json
import datetime
from Database import DataBase
class BmsAvailableSeats:
    def ticketsinfo(self,starts,stops):
        connection=DataBase().connection()
        cursor = connection.cursor()
        date=datetime.date.today()
        date=str(date)
        date=date.replace("-", "")
        query=""
        # print date
        seats_ssid="SELECT theater_code ,showdate,showtime,sessionid FROM collections.bms_showtimes where showdate =CURDATE() AND STR_TO_DATE(showtime,'%l:%i %p') BETWEEN SUBTIME(ADDTIME(current_time(),'5:30:00.00'),5900) AND  ADDTIME(ADDTIME(current_time(),'5:30:00.00'),5900) group by sessionid limit "+str(starts)+" , "+str(stops)
        print seats_ssid
        cursor.execute(seats_ssid)
        results = cursor.fetchall()
        # print "length======================================================================================",len(results)
        for j in results:
                print j[0]
                url="https://in.bookmyshow.com/serv/getData?cmd=GETSHOWINFO&vid="+j[0]+"&ssid="+str(j[3])
                print url
                r=requests.get(url)
                data = r.text
                val=""
                myjson=json.loads(data.replace("arrShowInfo=","")[:-1])
                # print "length==",len(myjson)
                for mjson in range(len(myjson)):
                    try:
                        tid= myjson[mjson][0]
                        ssid= myjson[mjson][1]
                        tc_class= myjson[mjson][2]
                        t_class= myjson[mjson][3]
                        price= myjson[mjson][4]
                        screen_name=myjson[mjson][33]
                        m=myjson[mjson].index(date)
                        l=myjson[mjson][m:]
                        totalseats=l[2]
                        availableseats=l[3]
                        val=val+"('"+tid+"','"+screen_name+"',"+"'"+ssid+"',"+"'"+tc_class+"',"+"'"+t_class+"',"+"'"+price+"',"+"'"+totalseats+"',"+"'"+availableseats+"'),"
                    except:
                        "DNA"          
                val=val[:-1]
                query=DataBase().seats_info+val
                # print query
                try:
                    cursor.execute(query)
                    connection.commit()
                    if cursor.lastrowid:
                            print('last insert id', cursor.lastrowid)
                    else:
                            print('last insert id not found') 
                            connection.commit()
                except:
                        print query
        #print "=================================================================="
    #print "------------------------------------------------------------------------------"
#database.db.close()    
