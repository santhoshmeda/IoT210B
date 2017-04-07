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

# http_client
# ipv4_udp_client message [ip_addr [port]]
print "\nhttps_client verb path [url [port]]"

# optional IP address
if len(sys.argv) > 1:
  HOST_IP = sys.argv[1]
else:
  HOST_IP = "0.0.0.0"

# optional port
if len(sys.argv) > 2:
  PORT = sys.argv[2]
else:
  PORT = 443


URL = "frozen-castle-53348.herokuapp.com"

conn = httplib.HTTPSConnection(URL, PORT)

conn.request('GET', '/api/v1/login')
r1 = conn.getresponse()
print "status " + str(r1.status) + ", reason " + str(r1.reason)
data1 = r1.read()
print "data: " + str(data1)
conn.close()
