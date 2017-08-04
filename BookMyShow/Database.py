'''
Created on 19-Jun-2017

@author: M Manoj
@contact: mmanoj@apikdd.com
'''
import mysql.connector
import sys
sys.path.append('../')
from dbconfig import *
class DataBase:

    connection=""
    '''
    Count Quries for Multi Thread 
    '''
    showtimesCountQuery="SELECT count(theater_code) as theater_code FROM collections.bms_theaters"
    '''
    Insert Quries using in code
    '''
    test="INSERT INTO pricefyi_test_results.bms_turls_test(urls,old_id) values "
    show_time_ssid="INSERT INTO collections.bms_showtimes(movie_code, movie_name, theater_code, theater_name, fullseat_layout, showdate, showtime, availability, sessionid) values "
    seats_info="INSERT INTO collections.bms_theatre_show_seats(theatre_code,screen_name,ssid,ticket_class_code,ticekt_class,price,total_seats,available_seats) VALUES "
    '''
    Select Quries using in code
    '''
    bms_estimator = "SELECT * FROM collections.bms_theatre_show_collections where collection is null;"
    trunk_ticket_info="truncate  collections.bms_theatre_show_seats"
    ssidcountquery="SELECT count(*) FROM collections.bms_showtimes where showdate =CURDATE() AND STR_TO_DATE(showtime, '%l:%i %p') BETWEEN SUBTIME(CURTIME(),5900) AND  ADDTIME(CURTIME(),5900)"
    def connection(self):
        try:
            connection = mysql.connector.connect(user=DEV_USER, passwd=DEV_PASSWD, db=DEV_DB, host=DEV_HOST)
            print "DataBase Connected"
        except:
            print "Connection Failed"
            print sys.exc_info()
        return connection
#print "hello"


