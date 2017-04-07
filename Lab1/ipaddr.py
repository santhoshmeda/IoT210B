#!/usr/bin/python
# =============================================================================
#        File : ipaddr.py
# Description : Displays IP addr on the Raspberry Pi SenseHat 8x8 LED display
#               e.g. '10.193.72.242'
#      Author : Drew Gislsason
#        Date : 3/1/2017
# =============================================================================

# To use on bootup of :
# sudo nano /etc/rc.local add line: python /home/pi/ipaddr.py &
#

from sense_hat import SenseHat
sense = SenseHat()
sense.set_rotation(180)
sense.show_letter('P')

# give time to get on the Wi-Fi network
import time
time.sleep(10)

# get our local IP address. Requires internet access (to talk to gmail.com).
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("gmail.com",80))
addr = s.getsockname()[0]
s.close()

# display that address on the sense had
sense.show_message(str(addr))
