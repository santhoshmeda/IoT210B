#!/usr/bin/python
# =============================================================================
#        File : ipv4_tcp_server.py
# Description : Displays whatever comes in on the TCP connection
#      Author : Drew Gislsason
#        Date : 3/8/2017
# =============================================================================
import socket
import sys

# ipv4_tcp_client message [ip_addr [port]]
print "\nipv4_tcp_server [ip_addr [port]]"

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

print "\nListening on IPv4 TCP port ", str(PORT)

# create TCP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind socket to port
server_addr = ('localhost', PORT)
print >>sys.stderr, 'starting up on %s port %s' % server_addr
sock.bind(server_addr)

# listen on the socket
sock.listen(12)

while True:
  # wait for a connection
  print >>sys.stderr, 'waiting for connection...'
  connection, client_addr = sock.accept()

  try:
    print >>sys.stderr, 'connection from', client_addr

    # receive the data
    while True:
      data = connection.recv(2048)
      if data:
        print "received (" + str(len(data)) + ") bytes data: " + data
      else:
        break

  finally:
    # TODO: send echo HTTP response

    # clean up
    print >>sys.stderr, 'closing connection'
    connection.close()
