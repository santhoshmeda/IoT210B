#!/usr/bin/python
# =============================================================================
#        File : ipv4_udp_server.py
# Description : UDP Server using sockets
#      Author : Drew Gislsason
#        Date : 3/8/2017
# =============================================================================
import socket
import sys
  
# ipv4_udp_client message [ip_addr [port]]
print "\nipv4_udp_server [ip_addr [port]]"

# optional IP address
if len(sys.argv) > 1:
  HOST_IP = sys.argv[1]
else:
  HOST_IP = "0.0.0.0"

# optional port
if len(sys.argv) > 2:
  PORT = sys.argv[2]
else:
  PORT = 5000

print "\nListening on IPv4 UDP port ", str(PORT)

sock = socket.socket(socket.AF_INET, # IPv4 Internet
            socket.SOCK_DGRAM) # UDP
sock.bind((HOST_IP, PORT))

while True:
  data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
  print "received (" + str(len(data)) + ") bytes from " + str(addr) + ": ", str(data) + "\n"
