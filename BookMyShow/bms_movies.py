'''
Created on 19-Jul-2017

@author: M Manoj
@contact: mmanoj@apikdd.com
'''
import sys
import re, datetime
import mysql.connector
import requests
from bs4 import BeautifulSoup
import specialCharacterConverter
from Database import DataBase
sys.path.append('../../')
from dbconfig import *
class BMS_movies:
    def getmovie(self,starts,stops):
        sql="SELECT id,city,theater_url,state from moviesfyi_stage.bk_theaters_final where theater_url is not null and id between "+str(starts)+" and "+str(stops)
        try:
            connection=DataBase().connection()
            cursor=connection.cursor()
            cursor.execute(sql)
            results=cursor.fetchall()
            for i in results:
                city=i[1]
        #         city="bengaluru"
                theater_url=i[2]
                state=i[3]
                url="https://in.bookmyshow.com/"+theater_url
        #         print url
                r=requests.get(url)
                data = r.text
                soup = BeautifulSoup(data,"lxml")
                
                for j in soup.find_all("ul",id="showEvents"):
                    try:
                        movies_ins=""
                        for k in j.find_all("div",class_="listing-info"):
        #                     print k
        #                     print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
                            lang=k.find("div",class_="eventInfo")
                            url=k.find("a")
                            languag=lang.text
                            mov_url=url["href"]
                            movie_url=mov_url
                            '''
                            BMS Movies Page
                            '''
                            qwe=requests.get("https://in.bookmyshow.com"+movie_url)
                            asdfg=qwe.text
                            moviecook=BeautifulSoup(asdfg,"lxml")
                            relda=moviecook.find("span",class_="__release-date").text
                            relda=relda.replace(",","")
                            relda=relda.replace(" ","-")
                            asd=relda.split("-")
                            releasedate= datetime.datetime.strptime(relda,'%d-%b-%Y').strftime('%Y-%m-%d')
                            gene=""
                            for bgen in moviecook.find_all("span", itemprop="genre"):
                                gene=gene+bgen.text+"|"
                            genere="|"+gene
                            censo=moviecook.find("span",class_="__censor")
                            senso=censo.find("use")
        #                     print senso
        #                     print "----------------------------"
                            sensor=senso["xlink:href"]
                            movie_censor=sensor[sensor.rindex("-")+1:]
                            movie_censor= movie_censor.upper()
                            mv_pstr=moviecook.find("div",class_="poster wow")
                            mov_posr=mv_pstr.find("meta")
                            movie_poster= mov_posr["content"]
                            movie_banner=movie_poster.replace("poster","banner")
        #                     print movie_banner
                            movie_tari=moviecook.find("div",class_="banner-main synopsis-banner")
                            movie_trailer_code=movie_tari["data-trailer-code"]
        #                     print movie_trailer_code
                            movie_trailer="https://www.youtube.com/watch?v="+movie_trailer_code
                            movie_description=moviecook.find("meta",itemprop="description")
                            movie_description= movie_description["content"]
                            movie_description=specialCharacterConverter.decode_unicode_references(movie_description)
                            movie_description=movie_description.replace("'","")
        #                     print movie_description
                            '''
                            Back to Theatres
                            '''
                            dimes=""
                            movie_code=movie_url[movie_url.rindex("/")+1:]
                            mov_url=mov_url.replace("/movies/","")
                            mov_url=mov_url.replace("/"+movie_code,"")
                            mov=url.text.strip()
                            deumlan=""
                            movie_dim="2D"
                            rm_lan="- "+languag
                            if rm_lan in mov:
                                movi=mov.replace(rm_lan,"")
                                if "(" in movi:
                                    deumlan=movi[movi.rindex("(")+1:]
                                    dimes=deumlan
                                    if " " in dimes:
                                        movie_dim=dimes.split(" ")
                                        movie_dim=movie_dim[0]
                                    else:
                                        movie_dim="2D"
                                    movi=movi.split("(")
                                    movi=movi[0]
                                    deumlan=deumlan.replace(")","").strip()
                                    deumlan=deumlan.replace(" ","-")
                                    deumlan=deumlan.lower()
                                    if deumlan in mov_url:
                                        mov_url=mov_url.replace("-"+deumlan,"")
                                    else:
                                        mov_url=mov_url
                                else:
                                    movi=movi
        #                     print languag
        #                     print mov_url
        #                     print movi
        #                     print movie_code
        #                     print releasedate
        #                     print movie_dim
                            movie_flag=city+movie_code
                            movies_ins=movies_ins+"('"+state+"','"+city+"','"+movi+"','"+genere+"','"+movie_censor+"','"+movie_banner+"', '', '"+movie_poster+"', '"+languag+"', '"+movie_dim+"', '"+releasedate+"', '"+movie_description+"', '"+movie_trailer+"', '', '','"+movie_code+"', '"+mov_url+"','"+movie_flag+"'),"
        #                     print "--------------------"
                        movies_ins=movies_ins[:-1]
        #                 print movies_ins
                        insmovieinfo="INSERT ignore INTO moviesfyi_stage.bk_movies (state, city, title, genre, censor, desktop_banner, mobile_banner, poster, language, dimension, release_date, description, trailer_url, rating, votes, movie_code, movie_url, book_groupcode) values "+movies_ins
#                         print  insmovieinfo
                        try:
                            cursor.execute(insmovieinfo)
                            connection.commit()
                        except:
                            print sys.exc_info()
        #                     print testurl
                            print insmovieinfo
                    except:
                        ""
        except:
            ""