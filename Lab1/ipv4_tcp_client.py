#!/usr/bin/python
# =============================================================================
#        File : ipv4_tcp_client.py
# Description : TCP client using sockets
#      Author : Drew Gislsason
#        Date : 3/8/2017
# =============================================================================
import socket
import sys

# ipv4_tcp_client message [ip_addr [port]]
if len(sys.argv) < 2:
  print "ipv4_tcp_client messge [ip_addr [port]]"
  exit()

# message is first argument
MESSAGE = sys.argv[1]

# IP address
if len(sys.argv) > 2:
  HOST_IP = sys.argv[2]
else:
  HOST_IP = "127.0.0.1" 

# port
if len(sys.argv) > 3:
  PORT = int(sys.argv[3])
else:
  PORT = 5000

print "\nipv4_tcp_client"
print "Target Host IP:", HOST_IP
print "Target Port:", PORT
print "Message:", MESSAGE

sock = socket.socket(socket.AF_INET, # Internet
          socket.SOCK_STREAM) # UDP
sock.connect((HOST_IP, PORT))
sock.send(MESSAGE)
