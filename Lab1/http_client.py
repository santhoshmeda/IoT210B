#!/usr/bin/python
# =============================================================================
#        File : https_client.py
# Description : Allows sending a verb with data to 
#      Author : Drew Gislsason
#        Date : 3/8/2017
# =============================================================================
import httplib
import base64
import sys

# http_client [

URL = "frozen-castle-53348.herokuapp.com"

conn = httplib.HTTPSConnection(URL, 443)

conn.request('GET', '/api/v1/login')
r1 = conn.getresponse()
print "status " + str(r1.status) + ", reason " + str(r1.reason)
data1 = r1.read()
print "data: " + str(data1)
conn.close()
