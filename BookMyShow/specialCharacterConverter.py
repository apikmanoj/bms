'''
Created on 19-Jul-2017

@author: M Manoj
@contact: mmanoj@apikdd.com
'''
import re
def _callback(matches):
   id = matches.group(1)
   try:
       return unichr(int(id))
   except:
       return id

def decode_unicode_references(data):
   return re.sub("&#(\d+)(;|(?=\s))", _callback, data)
